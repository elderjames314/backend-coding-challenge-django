from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note 
        fields = [
            'title',
            'body',
            'tags',
            'first_five_letter_title'
        ]