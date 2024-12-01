from django import forms
from django.contrib.auth.models import User
from .models import Ad, Category, Comment

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    nickname = forms.CharField(required=True, max_length=50)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'nickname', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords must match.')
        return password2

class AdForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    text = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField(required=False)

    class Meta:
        model = Ad
        fields = ('title', 'category', 'text', 'image')

class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('text',)