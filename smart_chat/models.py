from django.db import models
from django.contrib.auth.models import User
from django.template import Context, Template

from utils.model_mixins import BaseSmartChatModelMixin
from utils.datetime import (
    timezone_exist,
    get_timezone_utc_offset
)
from utils.generics import matches_regex


class Store(BaseSmartChatModelMixin, models.Model):
    """
    model for a store
    """
    name = models.CharField(max_length=100, null=False, blank=False)
    # sample fo time zone US/Hawaii
    timezone = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=25, null=False, blank=False)

    def clean(self):
        if self.timezone and not timezone_exist(self.timezone):
            raise ValueError("Unknown time zone")

    def save(self, *args, **kwargs):
        self.clean()
        super(Store, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Discount(BaseSmartChatModelMixin, models.Model):
    """
    discount code by store
    """
    store = models.OneToOneField(
        Store,
        on_delete=models.CASCADE,
    )
    discount_code = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.discount_code


class Operator(BaseSmartChatModelMixin, models.Model):
    """
    an representive of a store
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    # can be Fk to an operator store model
    operator_group = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.user.username

    class Meta:
        indexes = [
             models.Index(fields=['user_id'])
        ]


class Client(BaseSmartChatModelMixin, models.Model):
    """
    an client to a store
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    timezone = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=25, null=False, blank=False)

    def __str__(self):
        return self.user.username

    def clean(self):
        if self.timezone and not timezone_exist(self.timezone):
            raise ValueError("Unknown time zone")

    def save(self, *args, **kwargs):
        self.clean()
        super(Client, self).save(*args, **kwargs)


class Conversation(BaseSmartChatModelMixin, models.Model):
    """
    a thread between an operator and a client
    """
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, blank=False,
        related_name='conversations')
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, blank=False,
        related_name='conversations')

    operator = models.ForeignKey(
        Operator, on_delete=models.CASCADE, blank=False,
        related_name='conversations')

    RECEIVED = 'recv'
    PROCESSING = 'proc'
    RESOLVED = 'resv'
    STATUS_CHOICES = (
        (RECEIVED, 'Received'),
        (PROCESSING, 'Processing'),
        (RESOLVED, 'Resolved'),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=4,
                              default=RECEIVED)
    # we use this to keep check of the timezone to respect when sending
    utc_offset = models.SmallIntegerField(default=0)

    def __str__(self):
        return f"{self.store}/{self.client}"

    def save(self, *args, **kwargs):
        self.clean()

        # set the utc_offset
        timezone = self.client.timezone or self.store.timezone
        if timezone:
            self.utc_offset = get_timezone_utc_offset(timezone)

        self.clean()
        super(Conversation, self).save(*args, **kwargs)


class Chat(BaseSmartChatModelMixin, models.Model):
    """
    a single text sent out in a conversation
    """

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, blank=False,
        related_name='chats')
    payload = models.CharField(max_length=300, null=False, blank=False)
    discount = models.ForeignKey(
        Discount, on_delete=models.CASCADE, blank=False,
        related_name='chats')
    RECEIVED = 'recv'
    PENDING = 'pend'
    SENT = 'sent'
    STATUS_CHOICES = (
        (RECEIVED, 'Received'),
        (PENDING, 'pending'),
        (SENT, 'sent'),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=4,
                              default=RECEIVED)

    def clean(self):
        if self.payload and not matches_regex(
                r"[A-zA-Z1234567890{}$%_/-\/~@#$%^&\s()!?\.]+", self.payload):
            raise ValueError("Invalid payload")

    def save(self, *args, **kwargs):
        self.clean()
        super(Chat, self).save(*args, **kwargs)

    @property
    def plain_text(self):
        # replace since user doesn't have full_name property
        payload = self.payload.replace("full_name", "get_full_name")
        template = Template(payload)
        conversation = self.conversation
        context = Context({
            "client": conversation.client, "operator": conversation.operator,
            "discount": conversation.store.discount
        })
        return template.render(context)


class Schedule(BaseSmartChatModelMixin, models.Model):
    """
    an attempt to send out a chat
    """
    chat = models.OneToOneField(
        Chat,
        on_delete=models.CASCADE,
    )
    sent_date = models.DateTimeField(null=True, blank=True)
