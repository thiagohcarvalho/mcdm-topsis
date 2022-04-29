from django.urls import path
from .views import my_view
from .views import topsis_score

urlpatterns = [
    path('', my_view, name='my-view'),
    path('score/', topsis_score, name='topsis-score')

]
