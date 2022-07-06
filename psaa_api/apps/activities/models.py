from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

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
        on_delete=models.DO_NOTHING, null=False
    )
    user = models.ForeignKey(
        User, related_name='activities_admin',
        on_delete=models.SET_NULL, null=True
    )
    reason = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['create_at']


@receiver(post_save, sender='schools.Student')
def create_activity(sender, instance, created, **kwargs):
    if created:
        type = 'Enrollment' if instance.status == 'active' else 'Drop out'
        activity = Activity.objects.create(
            type=type,
            student=instance,
            school=instance.school,
            user=instance.user,
            reason=instance.comment
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
            reason=instance.comment
        )
        activity.save()
