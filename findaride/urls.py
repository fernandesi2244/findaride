from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import TemplateView
import django_cas_ng.views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('accounts/logout/', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
    path('auth/', include("users.urls")),
    path('api/', include("api.urls")),
    re_path(
        r"^.*$",
        TemplateView.as_view(template_name="base.html")
    )
]