from django.urls import path
from . import views
app_name = 'document'
urlpatterns = [
    path('', views.add_document, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('',views.sign_up , name='signup'),
    # path('login/',views.user_login , name='login'),
    # path('logout/',views.user_logout, name='logout'),
    path('document/<int:document_id>/', views.document_version, name='document_version'),
    path('document/update/<int:document_id>/', views.update_doc, name='update_doc'),
    path('document/delete/<int:document_id>/', views.delete_document, name='delete_document'),
    path('document/<int:document_id>/share/', views.share_document, name='share'),
    path('document/share/', views.shared_documents_list, name='shared'),
    path('document/download/<path:file_path>/', views.download_document, name='download_file'),
    path('document/share/permission/<int:document_id>/', views.permission, name='permission'),
    path('serve_document/<int:document_version_id>/', views.serve_document, name='serve_document'),

]
