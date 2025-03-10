"""
URL configuration for tejorder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('sunil/', include('sunil.urls')),
    path('hotel/', include('hotel.urls')),
    path('ajax/', include('ajax.urls')),
    path('waiter/', include('waiter.urls')),
    path('chef_helper/', include('chef_helper.urls')),
    path('download/', include('download.urls')),
    path('table_qr/', include('table_qr.urls')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = 'home.views.handling_404'