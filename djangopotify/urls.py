from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.contrib import admin

def homepage(request):
  return HttpResponse("<h1>Djangopotify - Home page</h1>")

urlpatterns = [
    path('', homepage),
    path('admin/', admin.site.urls),
    path('app/audios/', include('audios.urls')),
    path('app/accounts/', include('accounts.urls')),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
