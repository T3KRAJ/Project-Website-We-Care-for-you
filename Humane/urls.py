from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name = 'home'),
    path('about/', views.about, name = 'about'),
    path('', include('core.urls')),
    path('', include('Blog.urls', namespace = 'blog')),
    path('', include('Confession.urls', namespace = 'confession')),
    path('accounts/', include('allauth.urls')),
    path('chat/', include('chatapp.urls'))

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)