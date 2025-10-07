from django.db import models
from cloudinary.models import CloudinaryField

# ---------- TEAM MEMBER ----------
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    # Replace ImageField with CloudinaryField
    image = CloudinaryField(
        'image',
        folder='team_members',
        blank=True,
        null=True,
        help_text='Upload an image for this team member.'
    )

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

# ---------- BOOK ----------
class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=100)

    # Replace FileField with CloudinaryField for PDFs
    pdf_file = CloudinaryField(
        'raw',  # Use 'raw' for PDF files
        folder='books',
        resource_type='raw',  # Important for non-image files
        help_text='Upload the book PDF file here.'
    )

    upload_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ---------- LEADERBOARD ----------
class Leader(models.Model):
    name = models.CharField(max_length=100)
    period = models.CharField(max_length=100)
    achievement = models.CharField(max_length=100)
    recommendation = models.CharField(max_length=100)

    # Replace ImageField with CloudinaryField
    image = CloudinaryField(
        'image',
        folder='leaders',
        blank=True,
        null=True,
        help_text='Upload an image for this leader.'
    )

    class Meta:
        ordering = ['-period']

    def __str__(self):
        return f"{self.name} ({self.period})"