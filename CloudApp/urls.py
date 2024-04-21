from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [path("", views.index, name="index"),  # Empty string for the root URL
    	   path("index.html", views.index, name="index"),
	       path("UserLogin", views.UserLogin, name="UserLogin"),
	       path("User.html", views.User, name="User"),
	       path("Register.html", views.Register, name="Register"),
	       path("Signup", views.Signup, name="Signup"),	    
	       path("LoginTOTPAction", views.LoginTOTPAction, name="LoginTOTPAction"),
	       path("UploadFile.html", views.UploadFile, name="UploadFile"),
	       path("UploadFileAction", views.UploadFileAction, name="UploadFileAction"),
           #path('upload-file/<str:username>/', views.UploadFileAction, name='upload_file'),
	       path("DownloadFile", views.DownloadFile, name="DownloadFile"),
	       path("DownloadFileAction", views.DownloadFileAction, name="DownloadFileAction"),
           path('EncryptionResults', views.EncryptionResults, name='EncryptionResults'), 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)