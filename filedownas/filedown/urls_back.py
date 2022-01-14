"""filedown URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,re_path
from . import view_back

urlpatterns = [
    path('admin/', admin.site.urls),
    path('s', view_back.ct),
    path('bk', view_back.per_page),
    path('start/', view_back.ho),
    path('wenjcl/', view_back.wenjcl),
    path('dlzc/', view_back.dlzc),
    path('', view_back.shouye),

    path('myp/', view_back.my_image),

    # path('fehome/', view.fehome),
    path('netcz/', view_back.netcz),
    re_path(r's/xiaz/(?P<id>[0.0.0.0-90.90.90.90]+)$', view_back.xiaz)
]
