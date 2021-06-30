import uuid
from django.db import models
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey

from core.models import Timestamped
# Create your models here.

User = get_user_model()


class Document(Timestamped):
    document = models.FileField(upload_to='documents/')

    class Meta:
        default_related_name = 'documents'
        verbose_name = 'document'
        verbose_name_plural = 'documents'

    def __str__(self):
        return f"{self.document.name}"


class Folder(Timestamped, MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    files = models.ManyToManyField(Document, through='FolderDocument',
                                   blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        default_related_name = 'folders'
        verbose_name = 'folder'
        verbose_name_plural = 'folders'

    def __str__(self):
        return f"{self.name}"


class FolderDocument(Timestamped):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'folderdocuments'
        verbose_name = 'folder document'
        verbose_name_plural = 'folder documents'
