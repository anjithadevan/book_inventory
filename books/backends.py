from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=kwargs['username'])
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(kwargs['password']):
                return user
        return None