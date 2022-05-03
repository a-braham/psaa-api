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
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            # 'phone_number': self.user.phone_number,
        }


class Student(models.Model):
    """Model for students"""
    name = models.CharField(max_length=255)
    birth_date = models.DateTimeField(null=False, blank=False)
    level = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, related_name='created_by',
        on_delete=models.SET_NULL, null=True
    )
    parent = models.ForeignKey(
        User, related_name='parent',
        on_delete=models.DO_NOTHING, null=False
    )
    school = models.ForeignKey(
        School, related_name='school',
        on_delete=models.DO_NOTHING, null=False
    )
    phone_number = models.CharField(
        max_length=128,
        blank=True,
        null=True
    )
    status = models.CharField(max_length=100, default='active')
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            "created_at",
        ]

    def admin(self):
        """Get user created the student"""
        return {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
        }

    def get_parent(self):
        """Get parent of the student"""
        return {
            'id': self.parent.id,
            'username': self.parent.username,
            'email': self.parent.email,
        }

    def get_school(self):
        """Get student school"""
        return {
            'id': self.school.id,
            'name': self.school.name,
            'status': self.school.status,
        }
