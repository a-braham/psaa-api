from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import serializers
import json

from sqlalchemy import true

from psaa_api.apps.activities.models import Activity
from psaa_api.apps.authentication.models import User

School = get_user_model()


class Isibo(models.Model):
    """Model for isibo"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        School, related_name='isibo_admin',
        on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at', ]

    def admin(self):
        """Get admin of the school"""
        return {
            'id': self.user.id,
            'name': self.user.username,
            'email': self.user.email,
            # 'phone_number': self.user.phone_number,
        }


class School(models.Model):
    """Model for schools"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, related_name='school_admin',
        on_delete=models.SET_NULL, null=True
    )
    teacher = models.ForeignKey(
        School, related_name='teacher',
        on_delete=models.SET_NULL, null=True
    )
    description = models.TextField()
    province = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    enrollments = models.IntegerField(default=0)
    dropouts = models.IntegerField(default=0)
    status = models.CharField(max_length=100, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at', ]
    def save_school(self):
        return self.save()

    def admin(self):
        """Get admin of the school"""
        return {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            # 'phone_number': self.user.phone_number,
        }

    def students(self):
        school = self.id
        students = Student.objects.filter(school=school).values()
        return students

    def activities(self):
        school = self.id
        activities = Activity.objects.filter(school=school).values()

        data = []
        for activity in activities:
            student = Student.objects.get(
                pk=activity['student_id']
            )
            isiboStudent = IsiboUsers.objects.filter(student_id=activity['student_id'])
            if not isiboStudent:
                activity['student'] = {
                    "id": student.id,
                    "name": student.name,
                    "gender": student.gender,
                    "birth_date": student.birth_date,
                    "email": student.email,
                    "parent": student.parent,
                    "phone_number": student.phone_number
                }
            else:
                activity['student'] = {
                    "id": student.id,
                    "name": student.name,
                    "email": student.email,
                    "parent": student.parent,
                    "phone_number": student.phone_number,
                    'isibo': {
                        # 'id': isibo.id,
                        # 'name': isibo.name
                    }
                }
            activity['teacher'] = {
                'id': self.teacher.id,
                'name': self.teacher.username,
                'email': self.teacher.email
            }
            data.append(activity)
        return data


class Student(models.Model):
    """Model for students"""
    name = models.CharField(max_length=255)
    birth_date = models.DateTimeField(null=False, blank=False)
    gender = models.CharField(max_length=100, blank=True, null=True)
    level = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, related_name='created_by',
        on_delete=models.SET_NULL, null=True
    )
    parent = models.CharField(max_length=255)
    school = models.ForeignKey(
        School, related_name='school',
        on_delete=models.DO_NOTHING, null=False
    )
    isibo = models.ForeignKey(
        Isibo, related_name='student_isibo',
        on_delete=models.DO_NOTHING, default=1
    )
    phone_number = models.CharField(
        max_length=128,
        blank=True,
        null=True
    )
    email = models.EmailField(default='')
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

    def get_isibo(self):
        """Get student isibo"""
        return {
            'id': self.isibo.id,
            'name': self.isibo.name,
        }


@receiver(post_save, sender=Student)
def enrollment(sender, instance, created, **kwargs):
    if created:
        school = School.objects.get(id=instance.school.id)
        school.enrollments += 1
        school.save()


@receiver(post_save, sender=Student)
def dropout(sender, instance, created, **kwargs):
    if not instance._state.adding and instance.status == 'inactive':
        school = School.objects.get(id=instance.school.id)
        school.dropouts += 1
        school.enrollments -=1
        school.save()


class IsiboUsers(models.Model):
    """Model for isibo users"""
    isibo = models.ForeignKey(
        Isibo, related_name='isibo',
        on_delete=models.CASCADE, null=False
    )
    student = models.ForeignKey(
        Student, related_name='isibo_student',
        on_delete=models.CASCADE, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at', ]
        db_table = "isibo_users"

    def get_isibo(self):
        """Get isibo"""
        return {
            'id': self.isibo.id,
            'name': self.isibo.name,
            'status': self.isibo.status,
        }

    def get_student(self):
        """Get the user"""
        return {
            'id': self.student.id,
            'name': self.student.name,
            'parent': self.student.parent,
            'email': self.student.email,
            'phone_number': self.student.phone_number,
        }

    def students(self):
        isibo = self.id
        students = Student.objects.filter(isibo=isibo).values()
        return students
