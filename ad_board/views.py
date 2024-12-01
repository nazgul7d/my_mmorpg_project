from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .models import User, Category, Ad, Comment
from .forms import UserRegistrationForm, AdForm, CommentForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            domain = current_site.domain
            email_body = f"Hi {user.username}, \n Please click the link below to confirm your registration: \n http://{domain}/accounts/activate/{user.pk}/"
            email = EmailMessage(
                subject='Activate your account',
                body=email_body,
                from_email='your_email@example.com',
                to=[user.email]
            )
            email.send()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def activate(request, pk):
    user = User.objects.get(pk=pk)
    user.is_active = True
    user.save()
    return render(request, 'activation_success.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Your account is not yet active'})
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

@login_required
def home(request):
    ads = Ad.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'home.html', {'ads': ads, 'categories': categories})

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the ad form with the logged-in user as author
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            return redirect('home')  # Redirect to home page after successful creation
    else:
        form = AdForm()
    return render(request, 'create_ad.html', {'form': form})
