from rest_framework import serializers

from smart_chat.models import (
    Chat,
    Conversation
)


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
        read_only_fields = ('id', )


class ConversationSerializer(serializers.ModelSerializer):
    operator_group = serializers.SerializerMethodField()
    chats = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = (
            'id',
            'store',
            'operator',
            'operator_group',
            'client',
            'status',
            'chats'
        )
        read_only_fields = ('id', )

    def get_operator_group(self, conversation):
        return conversation.operator.operator_group

    def get_chats(self, conversation):
        chats = conversation.chats.all()
        return ChatSerializer(chats, many=True).data
