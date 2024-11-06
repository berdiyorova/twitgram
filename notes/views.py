from django.db.models import Q
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
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

    def get(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        queryset = self.get_queryset()

        search_term = request.query_params.get('search', None)
        if search_term:
            self.queryset = self.queryset.filter(text__icontains=search_term)

        page_obj = paginator.paginate_queryset(queryset, request)

        serializer = NoteSerializer(page_obj, many=True)
        return paginator.get_paginated_response(serializer.data)


class NotesAdminView(generics.ListAPIView):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAdminUser,]

    def get(self, request, *args, **kwargs):
        search_term = request.query_params.get('search', None)
        if search_term:
            self.queryset = self.queryset.filter(
                Q(text__icontains=search_term) |
                Q(user__username__icontains=search_term)
            )

        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(self.queryset, request)

        serializer = NoteSerializer(page_obj, many=True)
        return paginator.get_paginated_response(serializer.data)


class NotesDetailAdminView(generics.RetrieveDestroyAPIView):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAdminUser,]
    lookup_url_kwarg = 'pk'
