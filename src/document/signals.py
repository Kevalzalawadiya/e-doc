from django.db.models.signals import pre_save
from django.contrib.auth.signals import user_logged_in, user_logged_out,user_login_failed
from django.contrib.auth.models import User
from .models import DocumentDetails,DocumentVersion,DocumentShared,DocumentTracking
from django.dispatch import receiver
from django.db.models.signals import pre_init,pre_save, pre_delete, post_init, post_save, post_delete

@receiver(post_save, sender=DocumentDetails)
def doc_end_save(sender, instance,created,**kwargs):
    print("---------------------------------------")
    print("Post save Signals...")
    print("Sender:", sender)
    print("Document ID :" , instance.id)
    print("Document Name :", instance.name)
    print("Created User :", instance.created_by)
    print("Document Description :", instance.description)
    print("Created Date :", instance.created_date)
    print(f'Kwargs: {kwargs}')    
    if created:
        action = 'Add New Document'
        user = instance.created_by
        DocumentTracking.objects.create(action=action, user=user)

  

    # obj = DocumentVersion.objects.create(doc = instance, version = 1.0)
    # print(obj)
    # obj.save()   
    
@receiver(post_save, sender=DocumentVersion)
def version_save(sender, instance,**kwargs):
    print("---------------------------------------")
    print("Post save Signals for Document Version...")
    print("Sender:", sender)
    print("Document ID :" , instance.id)
    print("Document Name :", instance.doc)
    print("File Name :", instance.file)
    print("Document version :", instance.version)
    print("Created Date :", instance.update_at)
    print("Created Date :", instance.doc.created_date)
    print(f'Kwargs: {kwargs}')    
    DocumentTracking.objects.create(action='Add Version', user=instance.doc.created_by)
   

@receiver(post_save, sender=DocumentShared)
def share_save(sender, instance,**kwargs):
    print("---------------------------------------")
    print("Post save Signals for Document Share...")
    print("Sender:", sender)
    print("Document ID :" , instance.id)
    print("Document Name :", instance.document)
    print("Sender Name :", instance.receiver)
    print("Receiver Name  :", instance.shared_user)
    print("Permission on View  :", instance.shared_doc_view)
    print("Permission on Edit  :", instance.shared_doc_update)
    print("Permission on Download  :", instance.shared_doc_download)
    print(f'Kwargs: {kwargs}')    
    DocumentTracking.objects.create(action='Document Shared', user=instance.receiver)
   
   

# @receiver(post_save, sender=DocumentVersion)
# def at_end_save(sender, instance, **kwargs):
#     print("---------------------------------------")
#     print("Post save Signals...")
#     print("Sender:", sender)
#     print("Document Name :", instance)
#     print("Document_id :", instance.doc.id)
#     print("Document Folder :" , instance.file)
#     print("created date:" , instance.doc.created_date)
#     print("Version:" , instance.version)
#     print(f'Kwargs: {kwargs}')
    
    # latest_version = DocumentVersion.objects.filter(doc = instance)
    # latest_version = DocumentVersion.objects.order_by(instance.version)[:1] 
    # print(latest_version)
    # new_version = latest_version + 1.0  # type: ignore
    # obj = DocumentVersion.objects.create(doc = instance , version= new_version)
    # obj.save()
# pre_save.connect(at_beginning_save, sender=DocumentDetails)



# @receiver(user_logged_in, sender=User)
# def login_success(sender, request, user,**kwargs):
#     print("---------------------------------------")
#     print("Logges-in Signals... Run Intro..")
#     print("Sender:", sender)
#     print("Request:",request)
#     print("User:" , user)
#     print("User Password :", user.password)
#     print(f'Kwargs: {kwargs}')
# # user_logged_in.connect(login_success, sender=User)

# @receiver(user_logged_out, sender=User)
# def login_out(sender, request, user,**kwargs):
#     print("---------------------------------------")
#     print("Logges-out Signals... Run outro..")
#     print("Sender:", sender)
#     print("Request:",request)
#     print("User:" , user)
#     print(f'Kwargs: {kwargs}')
# # user_logged_out.connect(login_success, sender=User)

# @receiver(user_login_failed)
# def login_failed(sender, credentials ,request,**kwargs):
#     print("---------------------------------------")
#     print("Logging failed Signals...")
#     print("Sender:", sender)
#     print("Request:",request)
#     print("Credentials:" , credentials)
#     print(f'Kwargs: {kwargs}')
# # user_login_failed.connect(login_failed)

# @receiver(pre_save, sender=User)
# def at_beginning_save(sender, instance, **kwargs):
#     print("---------------------------------------")
#     print("Pre save Signals...")
#     print("Sender:", sender)
#     print("Instance:" , instance)
#     print(f'Kwargs: {kwargs}')
# pre_save.connect(at_beginning_save, sender=User)






