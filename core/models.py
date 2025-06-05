from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Custom User Model
class User(AbstractUser):
        ROLE_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('testing', 'Testing'),
        ('ads', 'Ads'),
    ]
        role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)

class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]
    REVIEW_STATUS_CHOICES = [
        ('NONE', 'None'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='individual_tasks')
    assigned_role = models.CharField(max_length=20, choices=User.ROLE_CHOICES, null=True, blank=True)



    # Submission and Review
    submitted_for_review = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    review_status = models.CharField(max_length=20, choices=REVIEW_STATUS_CHOICES, default='NONE')
    final_description = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    changes_description = models.TextField(blank=True, null=True)
    def get_assigned_users(self):
        if self.assigned_role:
            return User.objects.filter(role=self.assigned_role)
        elif self.assigned_to:
            return [self.assigned_to]
        return []

    def __str__(self):
        return self.title
class PendingUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # store hashed later if needed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()  # ✅ This is the actual field name
    created_at = models.DateTimeField(auto_now_add=True)


class TaskProgress(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='progress')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed')], default='PENDING')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('task', 'user')


class Profile(models.Model):
    ROLE_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('testing', 'Testing'),
        ('ads', 'Ads'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.user.username