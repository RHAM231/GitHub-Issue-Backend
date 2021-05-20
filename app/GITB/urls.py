from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('Sync/', include('sync.urls')),
    path('API/', include('consume_api.urls')),
    path('Issues/', include('issues.urls')),
    path('Repositories/', include('repositories.urls')),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
