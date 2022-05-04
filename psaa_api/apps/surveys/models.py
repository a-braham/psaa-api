from pyexpat import model
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Survey(models.Model):
    """Model for survey"""
    type = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, related_name='creator',
        on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    description = models.TextField()
    province = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    birth_date = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at', ]

    def admin(self):
        """Creator of the survey"""
        return {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            # 'phone_number': self.user.phone_number,
        }
