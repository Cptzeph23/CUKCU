from django.db import models
from cloudinary.models import CloudinaryField
import cloudinary

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

#---------BOOK------------------
class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=100)

    pdf_file = CloudinaryField(
        'raw',
        folder='books',
        resource_type='raw',
        blank=False,
        null=False,
        help_text='Upload the book PDF file here.',
        use_filename=True,  # Keep original filename
        unique_filename=False,  # Don't modify filename
    )

    upload_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_secure_pdf_url(self):
        """Get a secure, accessible PDF URL"""
        if self.pdf_file:
            try:
                # Generate a secure URL
                return cloudinary.utils.cloudinary_url(
                    self.pdf_file.public_id,
                    resource_type='raw',
                    type='upload',
                    secure=True,
                    sign_url=False  # Try both True and False
                )[0]
            except Exception as e:
                # Fallback to direct URL
                return self.pdf_file.url
        return None

    @property
    def pdf_download_url(self):
        """Property for template access"""
        return self.get_secure_pdf_url()

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