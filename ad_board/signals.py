from django.contrib.auth.signals import user_registered
from django.dispatch import receiver
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .models import User, Comment
from django.db.models.signals import post_save 

@receiver(user_registered)
def send_activation_email(sender, user, request, **kwargs):
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

@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:
        ad = instance.ad
        user = ad.author
        email_body = f"{instance.author.username} has left a comment on your ad: {ad.title} \n You can view the comment here: http://your_domain.com/ad/{ad.pk}/"
        email = EmailMessage(
            subject='New comment on your ad',
            body=email_body,
            from_email='your_email@example.com',
            to=[user.email]
        )
        email.send()