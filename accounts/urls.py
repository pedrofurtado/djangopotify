from django.urls import path, include
from . import views as accounts_views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', accounts_views.signup, name='signup'),
]
