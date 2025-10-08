from datetime import datetime, timedelta

from django.db import models
from cloudinary.models import CloudinaryField
import cloudinary



#----------CONTACT------------------
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name

#----------TEAM---------------------
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

    # --- NEW FIELD FOR CUSTOM SORTING ---
    order_index = models.IntegerField(
        default=99,
        verbose_name="Display Order",
        help_text="Enter a number to define the display order (e.g., Chairman=1, V. Chairman=2, Sec=3)."
    )

    # --- DEFINE SORTING IN META CLASS ---
    class Meta:
        # This is the line that defines the default sorting for all queries.
        # It sorts primarily by 'order_index' (ascending) and then by 'name'.
        ordering = ['order_index', 'name']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.position} - {self.name}"


#---------BOOK------------------
# models.py
class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=100)

    # Cloudinary field for PDF file
    pdf_file = cloudinary.models.CloudinaryField(
        'pdf',
        resource_type='raw',
        folder='books',
        blank=True,
        null=True,
        type = 'upload',
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_signed_pdf_url(self):
        if self.pdf_file:
            # Generate a signed URL that expires (e.g., in 1 hour)
            return self.pdf_file.build_url(
                secure=True,
                expires_at=datetime.now() + timedelta(hours=1)
            )
        return None


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