from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from flexxi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    #path('special/',views.special,name='special'),
    path('logout/', views.user_logout, name='logout'),
    path('flexxi/', include('flexxi.urls'), name='flexxi'),
]

if	settings.DEBUG:				
    urlpatterns	+=	static(settings.MEDIA_URL,														
    document_root=settings.MEDIA_ROOT)