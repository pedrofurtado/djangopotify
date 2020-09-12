from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from .models import Audio

class AudioListView(ListView):
    model = Audio
    template_name = 'audios/list.html'
    context_object_name = 'audios'

class AudioCreateView(CreateView):
    model = Audio
    fields = '__all__'
    template_name = 'audios/create.html'
    def get_success_url(self):
        return reverse_lazy('audios-detail', kwargs={'pk': self.object.id})

class AudioDetailView(DetailView):
    model = Audio
    template_name = 'audios/detail.html'
    context_object_name = 'audio'

class AudioUpdateView(UpdateView):
    model = Audio
    template_name = 'audios/update.html'
    context_object_name = 'audio'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('audios-detail', kwargs={'pk': self.object.id})

class AudioDeleteView(DeleteView):
    model = Audio
    template_name = 'audios/delete.html'
    success_url = reverse_lazy('audios-list')
