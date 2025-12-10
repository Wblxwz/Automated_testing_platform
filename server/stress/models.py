from django.db import models

# Create your models here.

class Project(models.Model):
    username = models.CharField(max_length=150)
    project_name = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)

class Stress(models.Model):
    project_id = models.IntegerField()
    stress_id = models.IntegerField()
    stress_status = models.CharField(max_length=150)
    create_time = models.DateField(auto_now_add=True)
    execute_time = models.DateTimeField(null=True, blank=True)
    run_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

class StressItem(models.Model):
    stress_name = models.CharField(max_length=200,unique=True)
    stress_command = models.TextField()
    stress_args = models.TextField()
    stress_label = models.TextField()
    stress_summary = models.TextField()
    