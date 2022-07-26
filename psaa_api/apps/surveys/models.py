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
            'phone_number': self.user.phone_number,
        }

    # def total_surveys(self):
    #     """Get total surveys"""
    #     surveys = Survey.objects.count()
    #     return surveys

    # def total_users(self):
    #     """Get total users"""
    #     users = User.objects.count()
    #     return users

    # def total_schools(self):
    #     """Get total schools"""
    #     pass

    # def drop_outs_vs_enrollments(self):
    #     """Get drops outs vs enrollments"""
    #     pass

    # def drop_out_by_gender(self):
    #     """Get drop outs by gender"""
    #     pass

    # def drop_out_causes(self):
    #     """Get drop out causes"""
    #     pass

    # def drop_out_by_school(self):
    #     """Get drop outs by school"""
    #     pass

    # def schools_inaccessibility_rate_by_districts(self):
    #     """Get schools inaccessibility rate by districts"""
    #     pass