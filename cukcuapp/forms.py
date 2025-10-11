# forms.py
from django import forms
from .models import TeamMember, Contact, Exec, Book





class ExecForm(forms.ModelForm):
    class Meta:
        model = Exec
        fields = ['name', 'position', 'bio', 'image', 'category']


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'position', 'bio', 'image', 'category']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'author', 'pdf_file']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
