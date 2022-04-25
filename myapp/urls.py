from django.urls import path
from .views import delete_files, my_view
from .views import topsis_score

urlpatterns = [
    path('', my_view, name='my-view'),
    path('/score/', topsis_score, name='topsis-score'),
    path('', delete_files, name='delete-files')
]
