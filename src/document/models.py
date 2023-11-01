from django.db import models
import datetime
from django.utils import timezone
from src.accounts.models import AdminUser
from django.core.files.storage import FileSystemStorage
from django.conf import settings 
# Create your models here.

class DocumentDetails(models.Model):
    created_by = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    def create_doc(self):
        return self.created_date >= timezone.now() - datetime.timedelta(days=1) 
    
class DocumentVersion(models.Model):
    doc = models.ForeignKey(DocumentDetails, on_delete=models.CASCADE)
    file = models.FileField(upload_to='E_document/',storage=FileSystemStorage(location=settings.MEDIA_ROOT))
    version = models.FloatField(default=1.0, null=True,blank=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.doc)
    
class DocumentShared(models.Model):
    document = models.ForeignKey(DocumentDetails, on_delete=models.CASCADE)
    receiver = models.ForeignKey(AdminUser, related_name='received_documents', on_delete=models.CASCADE)
    shared_user = models.ForeignKey(AdminUser,related_name='shared_documents',on_delete=models.CASCADE)
    shared_doc_view = models.BooleanField(default=False)
    shared_doc_update = models.BooleanField(default=False)
    shared_doc_download = models.BooleanField(default=False)
    def __str__(self):
        return f'Shared Document: {self.document.name} from {self.shared_user} to {self.receiver}'

class DocumentTracking(models.Model):
    action = models.CharField(choices=[('Add New Document','Add New Document'),('Add Version','Add Version'),('Document Shared','Document Shared'),('View','View'),('Edit','Edit'),('Download','Download'),('Delete','Delete')],max_length=200)
    created_date =  models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AdminUser,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user} performed {self.action} on {self.created_date}'
        

