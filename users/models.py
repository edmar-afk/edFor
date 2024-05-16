from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import FileExtensionValidator
# Create your models here.

now = timezone.now()

class Classroom(models.Model):
    class_name = models.CharField(max_length=250)
    section = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    room_code = models.CharField(max_length=250)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructor')
    students = models.ManyToManyField(User)
    
    def verify_room_code(self, entered_room_code):
        """
        Verify if the entered room code matches the classroom's room code.
        """
        return self.room_code == entered_room_code
    
class Activity(models.Model):
    room = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    description = models.TextField()
    posted = models.DateTimeField(default=now)
    deadline = models.DateField(blank=True)
    
    def user_has_submitted_file(self, user):
        """
        Check if the given user has already submitted a file for this activity.
        """
        return self.passactivity_set.filter(submitBy=user).exists()
   
class PassActivity(models.Model):
    activity_name = models.ForeignKey(Activity, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg', 'docx', 'ppt', 'xls'])],)
    submitBy = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    
class Lesson(models.Model):
    title = models.CharField(max_length=1000)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    description = models.TextField()
    lesson_file = models.FileField(upload_to='media/',blank=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg', 'docx', 'ppt', 'xls'])])
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=now)