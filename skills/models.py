from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Skill(models.Model):
    CATEGORY_CHOICES = (
        ('TECH', 'Technology'),
        ('ART', 'Arts'),
        ('MEDIA', 'Media'),
        ('SPORT', 'Sports'),
    )
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.category})"

class StudentSkill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        unique_together = ('user', 'skill')

    @property
    def level(self):
        if 1 <= self.rating <= 3:
            return 'BEGINNER'
        elif 4 <= self.rating <= 7:
            return 'INTERMEDIATE'
        elif 8 <= self.rating <= 10:
            return 'ADVANCED'
        return 'UNKNOWN'

    def __str__(self):
        return f"{self.user.username} - {self.skill.name} ({self.rating})"
