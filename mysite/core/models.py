from django.db import models
from .validators import validate_file_extension

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='books/pdfs/', validators=[validate_file_extension])
    cover = models.ImageField(upload_to='books/covers/', null=True, blank=True)
    index_number = models.CharField(max_length = 100, default = 'index')
    publisher = models.CharField(max_length = 100, default = 'Unknown')
    search_data = models.TextField(default='No Search Data')

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)
