from django.urls import path

from core.patterns import get_patterns
from .views import IndexView, delete_file, add_files


app_name = 'dms'
urlpatterns = get_patterns(app_name, 'views') + [
    path('', IndexView.as_view(), name="index"),
    path('delete/<int:folder>/<int:document>/', delete_file,
         name="delete_file"),
    path('add/files/<int:folder>/', add_files,
         name="add_files")
]
