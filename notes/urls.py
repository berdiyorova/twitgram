
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from notes import views

router = DefaultRouter()
router.register(r'', views.NoteViewSet)

urlpatterns = [
    path('note/', include(router.urls)),
    path('notes/', views.NotesAdminView.as_view()),
    path('notes/<int:pk>/', views.NotesDetailAdminView.as_view()),
]