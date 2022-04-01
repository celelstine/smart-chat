from datetime import datetime


from celery import shared_task
from celery.utils.log import get_task_logger

from django.db.models import Q
from django.conf import settings

from smart_chat.models import Schedule

logger = get_task_logger(__name__)

CHAT_ACTIVE_HOUR_BOUNDS = 8, 20


@shared_task(name="send_chats")
def send_chats():
    """
    task to send chats to client hoourly
    """
    logger.info("fetching chats to send")

    # get current time
    utc_naive_time_hour = datetime.now().hour

    # get bound of timezone offset within working hours 9am to 8pm (20:00)
    utc_offset_lower_bound = CHAT_ACTIVE_HOUR_BOUNDS[0] - utc_naive_time_hour
    utc_offset_upper_bound = CHAT_ACTIVE_HOUR_BOUNDS[1] - utc_naive_time_hour

    # get the schedules that not sent with conversation in the utcoffset bound
    schedules = Schedule.objects.filter(
        Q(chat__conversation__utc_offset__gte=utc_offset_lower_bound)
        |
        Q(chat__conversation__utc_offset__lte=utc_offset_upper_bound),
        sent_date__isnull=True
    )[:settings.MAX_CHAT_SCHEDULE_SEND]

    logger.info(f"sending {schedules.count()} chats")

    # for each schedule, call send_chat
    for schedule in schedules:
        send_chat.delay(schedule.pk)


@shared_task
def send_chat(schedule_id):
    logger.info(f"schedule_id {schedule_id} chats")
    schedule = Schedule.objects.get(pk=schedule_id)
    logger.info(f"schedule_id {schedule.__dict__} chats")
    chat = schedule.chat
    logger.info(
        f"sending chat {chat.plain_text} to \
            {chat.conversation.client.phone_number}")
    # call api to send the text
    schedule.sent_date = datetime.now()     # this is utc
    schedule.save()
