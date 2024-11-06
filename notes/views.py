from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from notes.models import NoteModel
from notes.serializers import NoteSerializer


class NoteViewSet(ModelViewSet):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class NotesAdminView(generics.ListAPIView):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAdminUser,]


class NotesDetailAdminView(generics.RetrieveDestroyAPIView):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAdminUser,]
    lookup_url_kwarg = 'pk'
