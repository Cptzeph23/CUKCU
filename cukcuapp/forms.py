# forms.py
from django import forms
from .models import TeamMember
from .models import Book



class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'position', 'bio', 'image', 'category']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description','author', 'pdf_file']

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField()

    def clean(self):
        email = self.cleaned_data.get('email')
        subject = self.cleaned_data.get('subject')
