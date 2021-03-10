"""Hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, re_path

from Hello.views import index, place_holder, human_face, random_pixels, mosaic


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('humanface64/', human_face),
    # ^[0-9]+x[0-9]+(#[0-9A-Fa-f]{6})?$
    re_path(r"^placeholder/(?P<width>[0-9]+)x(?P<height>[0-9]+)_(?P<color>([0-9A-Fa-f]{6}))/$",
            place_holder),
    re_path(r"^random_pixels/(?P<w>[0-9]+)x(?P<h>[0-9]+)@(?P<cell_size>[0-9]+)_(?P<color>([0-9A-Fa-f]{6}))/$",
            random_pixels),
    re_path(r"^mosaic/(?P<w>[0-9]+)x(?P<h>[0-9]+)@(?P<cell_size>[0-9]+)_(?P<color>([0-9A-Fa-f]{6}))/$", mosaic)
]






