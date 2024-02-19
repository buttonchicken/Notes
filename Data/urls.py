from django.urls import path
from .views import *

urlpatterns = [
    path('create', CreateNote.as_view()),
    path('edit/<note_id>', EditNote.as_view()),
    path('delete',DeleteNote.as_view()),
    path('<note_id>',GetNote.as_view()),
    path('share/<note_id>',ShareNotes.as_view()),
    path('version-history/<note_id>',GetNoteHistory.as_view()),
]