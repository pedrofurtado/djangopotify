from django.urls import path
from . import views

urlpatterns = [
    path('', views.AudioListView.as_view(), name='audios-list'),
    path('create', views.AudioCreateView.as_view(), name='audios-create'),
    path('<int:pk>', views.AudioDetailView.as_view(), name='audios-detail'),
    path('<int:pk>/update', views.AudioUpdateView.as_view(), name='audios-update'),
    path('<int:pk>/delete', views.AudioDeleteView.as_view(), name='audios-delete'),
]
