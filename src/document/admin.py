from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import DocumentDetails, DocumentVersion,DocumentShared,DocumentTracking
from django.contrib.auth.models import User , Group
from django.contrib.auth.models import Permission


class DocumentVersionInline(admin.TabularInline):
    model = DocumentVersion
    fields = ("version", "file")
    # readonly_fields = ("created_date",)
    extra = 1

class DocumentDetailsAdmin(admin.ModelAdmin):
    inlines = [ DocumentVersionInline ]
    
    def edit(self, obj):
        url = reverse('admin:document_documentdetails_change', args=[obj.id])
        return format_html('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"> <a class="btn btn-link" href="{}"> <i class="fa fa-bars"></i>  </a>', url)

    def delete(self, obj):
        url = reverse('admin:document_documentdetails_delete', args=[obj.id])
        return format_html('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"> <a class="btn btn-link" href="{}"> <i class="fa fa-trash"></i></a>', url)
    
    list_display_links = None
    list_display = ('id','created_by','name', 'description', 'created_date', 'delete' , 'edit')


class DocumentTrackingAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'created_date')


admin.site.register(DocumentDetails, DocumentDetailsAdmin)
admin.site.register(DocumentVersion)
admin.site.register(DocumentShared)
admin.site.register(DocumentTracking,DocumentTrackingAdmin)
# admin.site.register(User)
# admin.site.unregister(Group)





# class DocumentDetailsAdmin(admin.ModelAdmin):
#     # fieldsets = [ (None, {"fields": ["name"]}),(None, {"fields": ["description"]}),]
#     list_filter = ["created_date"]
#     search_fields = ["name"]
    