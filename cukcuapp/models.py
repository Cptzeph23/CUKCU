from django.db import models

# Create your models here.
# models.py
from django.db import models
from django.core.validators import FileExtensionValidator


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='media/')
    category = models.CharField(
        max_length=50,
        choices=[
            ('executive', 'Executive Committee'),
            ('ministerial', 'Ministerial Leaders'),
        ],
        default='ministerial',
    )

    def __str__(self):
        return self.name
class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=100)
    pdf_file = models.FileField(
        upload_to='books/pdfs',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text='Upload a book in PDF format'
    )
    upload_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

class Leader(models.Model):
    name = models.CharField(max_length=100)
    period = models.CharField(max_length=100)
    achievement = models.CharField(max_length=100)
    recommendation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='leaderboard/')

    class Meta:
        ordering = ['-period']

        def __str__(self):
            return f"{self.name} ({self.period})"












