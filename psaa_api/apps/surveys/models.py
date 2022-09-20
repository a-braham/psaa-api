from pyexpat import model
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Survey(models.Model):
    """Model for survey"""
    type = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, related_name='creator',
        on_delete=models.SET_NULL, null=True
    )
    isibo = models.ForeignKey(
        'schools.Isibo', related_name='survey_isibo',
        on_delete=models.DO_NOTHING, null=True
    )
    school = models.ForeignKey(
        'schools.School', related_name='survey_school',
        on_delete=models.DO_NOTHING, null=True
    )
    name = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    description = models.TextField()
    birth_date = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=255)
    parent = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
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

    def get_school(self):
        """Get student school"""
        return {
            'id': self.school.id,
            'name': self.school.name,
            'status': self.school.status,
        }

    def get_isibo(self):
        """Get student isibo"""
        return {
            'id': self.isibo.id,
            'name': self.isibo.name,
        }

    # @receiver(post_save, sender=Survey)
    # def survey(sender, instance, created, **kwargs):
    #     if created:
    #         # student = Student.objects.get(id=instance.student.id)
    #         survey = {
    #             type : instance.type,
    #             survey.reason : instance.reason,
    #             # student : student
    #         }
    #         survey.save()

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