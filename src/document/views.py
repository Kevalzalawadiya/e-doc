from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseNotFound,HttpResponse
from .forms import DocumentShareForm 
from django.template import loader
from src.accounts.models import AdminUser
from django.contrib.auth.forms import AuthenticationForm
from .models import DocumentDetails,DocumentVersion,DocumentShared,DocumentTracking
from django.contrib import messages
import os
from django.conf import settings 
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
import mimetypes


# Create your views here.
# def sign_up(request):
#     if request.method == "POST":
#         username= request.POST.get('username')
#         first_name= request.POST.get('first_name')
#         last_name= request.POST.get('last_name')
#         email= request.POST.get('email')
#         password1= request.POST.get('password1')
#         password2= request.POST.get('password2')
#         if password1 == password2:
#             if AdminUser.objects.filter(username=username).exists():
#                 messages.info(request, 'Username is already taken')
#                 return redirect('document:signup')
#             elif AdminUser.objects.filter(email=email).exists():
#                 messages.info(request, 'Email is already taken')
#                 return redirect('document:signup')
#             else:
#                 userdetails = AdminUser.objects.create_user(username=username, password=password1, 
#                                         email=email, first_name=first_name, last_name=last_name)
#                 userdetails.save()
#                 print(userdetails)
#                 return redirect('document:login')
#         else:
#             messages.info(request, 'Both passwords are not matching')
#             return redirect('document:signup')
#     else:
#         print("last else")
#         return render (request,'document/signup.html')

# def user_login(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request=request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username = username , password = password)
#             if user is not None:
#                 login(request,user)
#                 return redirect('document:dashboard')
#     return render(request,'document/login.html')
   
# def user_logout(request):
#     logout(request)
#     return redirect('document:login')

def dashboard(requrst):
    user = AdminUser.objects.all()
    if requrst.user != user:  
        return render(requrst,'document/dashboard.html')
    else:
        return redirect('document:home')

@login_required
def add_document(request):
        if request.method == 'POST':
            name= request.POST.get('name')
            description= request.POST.get('description')
            docdetails = DocumentDetails(name = name,
                                    description = description,
                                    created_by=request.user
                                    )
            docdetails.save()
        document= DocumentDetails.objects.filter(created_by=request.user)
        if request.method == 'GET':
            query = request.GET.get('search')
            if query!= None:
                document = DocumentDetails.objects.filter(name__icontains=query)
        template = loader.get_template("document/home.html")
        return render(request,'document/home.html',{'document':document})

@login_required    
def update_doc(request,document_id):
        doc = DocumentDetails.objects.get(pk=document_id)
        if request.method == 'POST':
            doc.name = request.POST.get('name')
            doc.description = request.POST.get('description')
            doc.save()
            return redirect('document:home')
        else:
            DocumentTracking.objects.create(action='Edit', user=request.user)
            return render(request, 'document/edit.html', {"doc": doc})
        
def delete_document(request, document_id):
    document = DocumentDetails.objects.get(id=document_id)
    if request.method == 'POST':
        document.delete()
        DocumentTracking.objects.create(action='Delete', user=request.user)
        return redirect('document:home')
    else:
        return render(request, 'document/delete.html')  
   
@login_required
def document_version(request, document_id):
        doc = DocumentDetails.objects.get(pk=document_id)
        versions = DocumentVersion.objects.filter(doc=doc)
        if request.method == 'POST':
            file = request.FILES.get('file')
            latest_version = 0
            try:
                latest_version = DocumentVersion.objects.filter(doc = doc).order_by("-version").first().version
            except:
                print(" you upload first file in this document")
            DocumentVersion.objects.create(doc = doc,file = file,
                                    version = latest_version +1.0)
        DocumentTracking.objects.create(action='View', user=request.user)     
        return render(request, 'document/view.html', {"doc": doc, "versions": versions})
    
@login_required
def serve_document(request, document_version_id):
    version = get_object_or_404(DocumentVersion, pk=document_version_id)
    file = version.file

    # Determine the file's content type
    content_type, _ = mimetypes.guess_type(file.name)

    response = FileResponse(file, content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file.name)}'

    return response


@login_required
def download_document(request,file_path):
    DocumentTracking.objects.create(action='Download', user=request.user)     
    path = os.path.join(settings.MEDIA_ROOT, file_path)   
    if os.path.exists(path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(),content_type ="application/file")
            response['Content-Disposition'] = 'inline; filename='+os.path.basename(path)
            return response
    else:
        return HttpResponseNotFound('File not found.')

    
@login_required
def share_document(request, document_id):
    document = DocumentDetails.objects.get(id=document_id)
    users = AdminUser.objects.all()
    if request.method == 'POST':
        form = DocumentShareForm(request.POST)
        if form.is_valid():
            shared_user = form.cleaned_data['shared_user']
            shared_doc_view = form.cleaned_data.get('shared_doc_view', False)
            shared_doc_update = form.cleaned_data.get('shared_doc_update', False)
            shared_doc_download = form.cleaned_data.get('shared_doc_download', False)
            shared_document = DocumentShared(
                document=document,
                receiver=request.user,
                shared_user=shared_user,
                shared_doc_view=shared_doc_view,
                shared_doc_update=shared_doc_update,
                shared_doc_download=shared_doc_download)
            shared_document.save()
            return redirect('document:home') 
    else:
        form = DocumentShareForm()
    
    return render(request, 'document/share.html', {'form': form, 'document': document, 'users':users})

@login_required
def shared_documents_list(request):
    shared_documents = DocumentShared.objects.filter(shared_user=request.user)
    print("--------------------->",shared_documents)
    if request.method == 'POST':
            query = request.POST.get('search')
            if query!= None:
                shared_documents = DocumentShared.objects.filter(document__name__icontains = query)
    template = loader.get_template("document/receive.html")
    return render(request, 'document/receive.html', {'shared_document': shared_documents})

@login_required
def permission(request, document_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        document = DocumentDetails.objects.get(id=document_id)
        shared_documents = DocumentShared.objects.filter(document=document, shared_user=request.user)
        for shared_document in shared_documents:
            if action == 'view' and shared_document.shared_doc_view:
                return redirect('document:document_version', document_id=document_id)            
            elif action == 'update' and shared_document.shared_doc_update:
                return redirect('document:update_doc', document_id=document_id)               
            elif action == 'download' and shared_document.shared_doc_download:
                return redirect('document:document_version', document_id=document_id)
            else:
                return redirect('document:shared')
    return render(request, 'document/receive.html')






