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
# models.py
class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=100)

    # Store the Cloudinary URL directly
    pdf_url = models.URLField(blank=True, null=True)
    pdf_public_id = models.CharField(max_length=255, blank=True, null=True)

    upload_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Handle file upload in save method
        if hasattr(self, '_pdf_file'):
            try:
                result = cloudinary.uploader.upload(
                    self._pdf_file,
                    resource_type='raw',
                    folder='books'
                )
                self.pdf_url = result['secure_url']
                self.pdf_public_id = result['public_id']
            except Exception as e:
                # Handle upload error
                pass
        super().save(*args, **kwargs)

    def get_pdf_url(self):
        return self.pdf_url


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