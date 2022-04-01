from rest_framework import viewsets

from smart_chat.models import (
    Chat,
    Conversation
)

from api.v1.serializers import (
    ChatSerializer,
    ConversationSerializer,
)

# ! TODO: setup authenticaton and limit objects to user's scope


class ChatViewSet(viewsets.ModelViewSet):
    """
    viewset for chats
    """
    serializer_class = ChatSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]

    def get_queryset(self):
        return Chat.objects.all().order_by('create_date')


class ConversationViewSet(viewsets.ModelViewSet):
    """
    viewset for Conversation
    """
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.all().order_by('create_date')
