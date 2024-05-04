from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """
    When a user logs in, we want to load their profile
    """
    request.session['user_id'] = user.username

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    """
    When a user logs out, the profile is no longer needed
    """
    del request.session['user_id']