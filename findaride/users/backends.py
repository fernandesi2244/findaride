from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django_cas_ng.backends import CASBackend

UserModel = get_user_model()

class CustomCASBackend(CASBackend):
    # only allow cas logins for now
    pass


class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        
        if username is None or password is None:
            return

        try:
            # DON'T CHECK THAT EMAIL IS VERIFIED FOR NOW
            #user = UserModel._default_manager.get(
            #    Q(email__iexact=username) & Q(email_verified=True)
            #)
            user = UserModel._default_manager.get(
                Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
