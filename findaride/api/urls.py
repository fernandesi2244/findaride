from django.urls import include, path
from .views import TripRequestModelViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'trip-request', TripRequestModelViewSet)

urlpatterns = [

]

urlpatterns += router.urls
