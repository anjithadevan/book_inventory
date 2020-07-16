from django.urls import include, path
from rest_framework import routers
from books import views

router = routers.DefaultRouter()
router.register(r'register_user', views.UserSignUpViewSet)
router.register(r'login_user', views.UserLoginViewset)

urlpatterns = [
    path('', include(router.urls)),
    ]