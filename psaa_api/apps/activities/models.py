from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from psaa_api.apps.surveys.models import Survey

User = get_user_model()


class Activity(models.Model):
    """Model for activities"""
    type = models.CharField(max_length=100)
    student = models.ForeignKey(
        'schools.Student', related_name='student',
        on_delete=models.SET_NULL, null=True
    )
    school = models.ForeignKey(
        'schools.School', related_name='activities_school',
        on_delete=models.DO_NOTHING, null=True
    )
    user = models.ForeignKey(
        User, related_name='activities_admin',
        on_delete=models.SET_NULL, null=True
    )
    isibo = models.ForeignKey(
        'schools.Isibo', related_name='activities_isibo',
        on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['create_at']


@receiver(post_save, sender=Survey)
def survey(sender, instance, created, **kwargs):
    if created:
        activity = Activity.objects.create(
            type=instance.type,
            name=instance.name,
            user=instance.user,
            school=instance.school,
            reason=instance.reason,
            # isibo=instance.isibo
        )
        activity.save()

@receiver(post_save, sender='schools.Student')
def create_activity(sender, instance, created, **kwargs):
    if created:
        type = 'Enrollment' if instance.status == 'active' else 'Drop out'
        activity = Activity.objects.create(
            type=type,
            student=instance,
            school=instance.school,
            user=instance.user,
            reason=instance.comment,
            isibo=instance.isibo
        )
        activity.save()


@receiver(post_save, sender='schools.Student')
def dropout(sender, instance, created, **kwargs):
    if not instance._state.adding and instance.status == 'inactive':
        type = 'Enrollment' if instance.status == 'active' else 'Drop out'
        activity = Activity.objects.create(
            type=type,
            student=instance,
            school=instance.school,
            user=instance.user,
            reason=instance.comment,
            isibo=instance.isibo
        )
        activity.save()
