from django.db import models

# Create your models here.
# models.py
from django.db import models

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
