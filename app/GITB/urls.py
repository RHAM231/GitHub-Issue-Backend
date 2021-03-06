"""
GITB URL Configuration

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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Django Apps
    path('', include('base.urls')),
    path('Sync/', include('sync.urls')),
    path('API/', include('consume_api.urls')),
    path('Issues/', include('issues.urls')),
    path('Repositories/', include('repositories.urls')),
    path('profile/', user_views.profile, name='profile'),

    # Standard Django user urls using user and auth_views
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logout.html'), name='logout'),

    # Enable media url for the site
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
