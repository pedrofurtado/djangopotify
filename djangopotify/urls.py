from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def homepage(request):
  return HttpResponse("<h1>Djangopotify - Home page</h1>")

urlpatterns = [
    path('', homepage),
    path('audios/', include('audios.urls')),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
