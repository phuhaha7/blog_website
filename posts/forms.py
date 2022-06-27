from ast import For
import imp
from django.forms import EmailInput, ModelForm, PasswordInput, Textarea, Form, CharField, TextInput
from . models import Post

class PostingForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['user','created_at',]
        widgets = {
            "body" : Textarea(attrs={'cols': 40, 'rows':10})}

class RegistrationForm(Form):
    username = CharField(max_length=20, required=True, widget=TextInput(attrs={'placeholder': 'username'}))
    email = CharField(widget=EmailInput(attrs={'placeholder': 'email'}), required=True)
    password = CharField(widget=PasswordInput(attrs={'placeholder': 'password'}))
    confirm_password = CharField(widget=PasswordInput(attrs={'placeholder': 'confirm password'}))