from django.contrib import admin

from smart_chat.models import (
    Store,
    Discount,
    Client,
    Operator,
    Conversation,
    Chat,
    Schedule
)


class DiscountInline(admin.StackedInline):
    model = Discount
    extra = 0
    fields = ('store', 'discount_code')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    inlines = [
        DiscountInline,
    ]
    list_display = (
        'id', 'name', 'timezone', 'phone_number', 'modify_date', 'create_date')
    readonly_fields = ('create_date', 'modify_date',)
    search_fields = ['id', 'name', 'timezone', 'phone_number']

    def get_queryset(self, request):
        return super(StoreAdmin, self).get_queryset(
            request).order_by('name')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'store', 'discount_code', 'modify_date', 'create_date')
    readonly_fields = ('create_date', 'modify_date',)
    search_fields = ['id', 'discount_code']


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'operator_group', 'modify_date', 'create_date')
    readonly_fields = ('create_date', 'modify_date',)
    search_fields = ['id', 'operator_group']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'timezone', 'phone_number', 'modify_date', 'create_date')
    readonly_fields = ('create_date', 'modify_date',)
    search_fields = ['id', 'user__first_name', 'timezone', 'phone_number']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'store', 'client', 'operator', 'utc_offset', 'status',
        'modify_date', 'create_date')
    readonly_fields = ('create_date', 'modify_date', 'utc_offset')
    search_fields = ['id', 'user__first_name', 'store__name', 'phone_number']


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'conversation', 'payload', 'status',
        'modify_date', 'create_date')
    readonly_fields = ('create_date', 'modify_date')
    search_fields = ['payload__icontains']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'chat', 'sent_date',
        'modify_date', 'create_date')
    readonly_fields = ('id', 'chat', 'sent_date', 'modify_date', 'create_date')

    # to make the form read only
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
