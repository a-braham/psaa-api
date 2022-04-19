from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class School(models.Model):
    """Model for schools"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, related_name='school_admin',
        on_delete=models.SET_NULL, null=True
    )
    description = models.TextField()
    province = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    enrollments = models.IntegerField(default=0)
    dropouts = models.IntegerField(default=0)
    status = models.CharField(max_length=100, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at', ]

    def admin(self):
        """Get admin of the school"""
        return {
            'username': self.user.username,
            'email': self.user.email,
            # 'phone_number': self.user.phone_number,
        }
