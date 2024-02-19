from .models import *
from rest_framework import serializers
from datetime import datetime, timedelta

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['note_id','note_data','created_at']

class NoteEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['note_data']

class NoteHistorySerializer(serializers.ModelSerializer):
    def get_last_updated_at(self, obj):
        updated_at_str = obj.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        dt = datetime.strptime(updated_at_str, "%Y-%m-%d %H:%M:%S")
        ist_dt = dt + timedelta(hours=5, minutes=30)
        formatted_updated_at = ist_dt.strftime("%d %b %Y %H:%M %p")
        return formatted_updated_at
    last_updated_at = serializers.SerializerMethodField()
    class Meta:
        model = NoteHistory
        fields = ['changed_data','last_updated_at']