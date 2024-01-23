from django import forms
from django.contrib.auth.forms  import UserCreationForm

from styleshines.models import User,Category,Jewellery,JewelleryVarients,Offers


# -----------------------Registration Form----------------------------------
class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2','phone','address']
        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "password1":forms.PasswordInput(attrs={"class":"form-control"}),
            "password2":forms.PasswordInput(attrs={"class":"form-control"}),
            "phone":forms.TextInput(attrs={"class":"form-control"}),
            "address":forms.TextInput(attrs={"class":"form-control"})
        }

# --------------------Login Form---------------------------------------------

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


# -----------------------Category Add Form-------------------------------------

class CategoryAddForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['category']

        widgets={
            "category":forms.TextInput(attrs={"class":"form-control"})
        }

# -----------------------Jewellery Add Form-----------------------------------------

class JewelleryAddForm(forms.ModelForm):
    class Meta:
        model=Jewellery
        fields='__all__'

# -----------------------Jewellery Varient Add Form------------------------------------

class JewelleryVarientsAddForm(forms.ModelForm):
    class Meta:
        model=JewelleryVarients
        exclude=('jewel',)

# ------------------Offers add Form--------------------------------------------------------

class OfferAddForm(forms.ModelForm):
    class Meta:
        model=Offers
        exclude=('jewel_varient',)
        widgets={
            'start_date':forms.DateInput(attrs={'type':'date'}),
            'end_date':forms.DateInput(attrs={'type':'date'})
        }
