from django.urls import path

from core.patterns import get_patterns
from .views import IndexView, delete_file


app_name = 'dms'
urlpatterns = get_patterns(app_name, 'views') + [
    path('', IndexView.as_view(), name="index"),
    path('delete/<int:folder>/<int:document>/', delete_file,
         name="delete_file")
]
