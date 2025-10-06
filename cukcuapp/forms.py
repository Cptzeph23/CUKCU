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
