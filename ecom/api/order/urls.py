from rest_framework import routers
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = routers.DefaultRouter()
router.register(r'', views.OrderViewSet)

urlpatterns = [
    path('add/<str:id>/<str:token>/', views.add, name='order.add'),
    path('', include(router.urls)),

]