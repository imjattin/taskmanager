from rest_framework import routers

from tasks.views import TaskViewSet

# Create a router and register the TaskViewSet with it
# This will automatically generate the URL patterns for the Task API endpoints
# The TaskViewSet should handle CRUD operations for the Task model
router = routers.DefaultRouter()
router.register(r"tasks", TaskViewSet)

urlpatterns = router.urls
