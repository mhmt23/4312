from django.db import models
from django.contrib.auth.models import User

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
