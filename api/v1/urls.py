from rest_framework.routers import DefaultRouter

from api.v1 import views


router = DefaultRouter()
router.register(r'chats', views.ChatViewSet, basename='chats')
router.register(
    r'conversations', views.ConversationViewSet, basename='conversations')

urlpatterns = router.urls
