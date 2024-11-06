from rest_framework import serializers

from notes.models import NoteModel


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteModel
        fields = '__all__'
        read_only_fields = ['user', 'created_at']
