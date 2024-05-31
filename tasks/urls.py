# tasks/urls.py
from rest_framework import routers
from .views import TaskViewSet, TaskesViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'taskes', TaskesViewSet, basename='taskes')

urlpatterns = router.urls
