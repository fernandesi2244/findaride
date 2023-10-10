from django.urls import path
from .views import *

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"), #login
    path("is-logged-in/", IsLoggedInView.as_view(), name="is-logged-in"), #isLoggedIn
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<str:token>/', ActivateUserView.as_view(), name='activate'),
]