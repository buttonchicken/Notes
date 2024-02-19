from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Create your models here.
class Note(models.Model):
    note_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    note_data = models.CharField(max_length=500)

class SharedNote(models.Model):
    shared_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name='shared_by')
    shared_with = models.ForeignKey(User,on_delete=models.CASCADE, related_name='shared_with')
    note = models.ForeignKey(Note,on_delete=models.CASCADE)

class NoteHistory(models.Model):
    note = models.ForeignKey(Note,on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)
    changed_data = models.CharField(max_length=500)