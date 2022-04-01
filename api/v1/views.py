from rest_framework import viewsets

from smart_chat.models import Chat

from api.v1.serializers import ChatSerializer


class ChatViewSet(viewsets.ModelViewSet):
    """
    viewset for chats
    """
    serializer_class = ChatSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]

    def get_queryset(self):
        return Chat.objects.all().order_by('create_date')
