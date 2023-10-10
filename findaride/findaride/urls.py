from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import TemplateView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("users.urls")),
    re_path(
        r"^.*$",
        TemplateView.as_view(template_name="base.html")
    )
]