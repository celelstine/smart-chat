from rest_framework.routers import DefaultRouter

from api.v1 import views


router = DefaultRouter()
router.register(r'chats', views.ChatViewSet, basename='chats')

urlpatterns = router.urls
