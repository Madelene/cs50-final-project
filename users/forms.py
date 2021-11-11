from django import forms as djforms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data["username"].lower()

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class LoginForm(djforms.Form):
    username = djforms.CharField(max_length=255, required=True)
    password = djforms.CharField(widget=djforms.PasswordInput, required=True)
    next_url = djforms.CharField(widget=djforms.HiddenInput(), required=False)

    def clean(self):
        username = self.cleaned_data.get('username').lower()
        password = self.cleaned_data.get('password')
        # logger.info("clean attempting {} // {}".format(username, password))
        user = authenticate(username=username, password=password)
        # logger.info("clean response ==  {}".format(user))
        if not user or not user.is_active:
            raise djforms.ValidationError(
                "Sorry, that login was invalid. Please try again."
            )
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username').lower()
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
