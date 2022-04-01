from rest_framework import serializers

from smart_chat.models import Chat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = (
            'id',
            'payload',
            'conversation',
            'create_date',
            'status',
        )
