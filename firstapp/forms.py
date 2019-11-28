from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import connection
from datetime import datetime
from django.core import validators,exceptions
from firstapp.models import User_extends,Product,AuthUser
from datetime import datetime

uname =None

class Userregistrtion(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

        labels={
            'username': "Univercity Number"
        }

        widgets={
            'username': forms.TextInput(attrs={'Placeholder':"Enter Univercity Seat Number"})
        }
    
    def save(self,commit=True):
        global uname
        uname = self.cleaned_data['username']
        user = super(Userregistrtion,self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user


class  UserExtendedForm(forms.ModelForm):
    profile = forms.FileField(label="Choose pic",required=False)
    class Meta:
        model = User_extends
        fields = ('gender','bdate','profile','address')
        labels ={
            'bdate':"Birth Date"
        }
        widgets={
          'bdate': forms.DateInput(attrs={'type': 'text','class': 'datepicker','autocomplete':"off"}),
          'address': forms.Textarea(attrs={'cols':5,'rows':2}) 
        }

    
    def save(self,Filename=None):
        global uname
        instance  = User_extends.objects.create(username=uname,gender=str(self.cleaned_data['gender']),bdate=str(self.cleaned_data['bdate']),myfile=str(Filename),address=str(self.cleaned_data['address']))

class Productform(forms.ModelForm):
    class Meta:
        model = Product
        fields= "__all__"
        exclude =('ID','username')
        widgets={
          'Upload_date'  : forms.TextInput(attrs={'Placeholder':str(datetime.date(datetime.now())),'type': 'text','class': 'datepicker','autocomplete':"off"}),
          'Description': forms.Textarea(attrs={'cols':5,'rows':2})
        }
    
    def save(self,userid):
        pass