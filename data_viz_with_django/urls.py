"""data_viz_with_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from viz import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.get_name, {}, name='index'),
    path('index.html', views.db_controller_view, {}, name='db_controller'),
    path('data_table.html', views.data_table_view, {}, name='data_table'),


    path('test.html', views.test_view, {}, name='test'),
    path('inherit_from_test.html', views.inherit_from_test_view, {}, name='inherit_test')
]

from django.urls import path
from viz import views


urlpatterns = [
    path('test.html', views.test_view, {}, name='test'),
    path('inherit_from_test.html', views.inherit_from_test_view, {}, name='inherit_test')
]
