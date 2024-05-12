from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import listing, imageGallery, account, forVerification

class createUser(UserCreationForm):

    class meta:

        model=User
        fields = ['username', 'email', 'password1', 'password2']


class imageForm(forms.ModelForm):

    class Meta:

        model=listing
        fields = ['primaryImage']

class galleryForm(forms.ModelForm):

    class Meta:

        model=imageGallery
        fields = ['image1', 'image2', 'image3', 'image4']

class profileForm(forms.ModelForm):

    class Meta:

        model=account
        fields = ['profilePicture']

class idForm(forms.ModelForm):

    class Meta:

        model=forVerification
        fields = ['frontPhoto', 'backPhoto']