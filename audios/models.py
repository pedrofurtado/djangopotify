from django.db import models

def audio_cover_upload_path(instance, filename):
    return 'audios/cover/{0}/raw_{1}'.format(instance.pk, filename)

class Audio(models.Model):
    name = models.CharField(max_length=255, null=True)
    cover = models.FileField(upload_to=audio_cover_upload_path, null=True)
