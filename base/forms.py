from django import forms
from .models import Room,User,Topic
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RoomForm(forms.ModelForm):
    new_topic = forms.CharField(required=False, max_length=100, label="Or add a new topic")
    class Meta:
        model=Room
        fields='__all__'
        # fields=['topic','new_topic','name','description']
        exclude=['host','participants']


class RegistrationForm(UserCreationForm):
    # Email = forms.EmailField( required=True)

    class Meta:
        model=User
        fields=['username','email','password1','password2']


class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','avatar']