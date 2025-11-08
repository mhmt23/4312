from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill, blank=True)
    time_credit = models.FloatField(default=0)

    def __str__(self):
        return self.user.username

class Service(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('request', 'Request'),
        ('offer', 'Offer'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPE_CHOICES)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_services')
    skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True)
    time_required = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_services')

    def __str__(self):
        return self.title

class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('service', 'reviewer') # A user can only review a service once

    def __str__(self):
        return f'Review by {self.reviewer.username} for {self.reviewee.username} on "{self.service.title}"'
