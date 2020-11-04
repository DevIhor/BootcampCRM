import logging

from celery import shared_task
from django.contrib.auth.models import User

logger = logging.getLogger("celery")


@shared_task
def create_log(user_id, log_type, log_msg):
    """Create log action with type `log_type` and message `log_message`
    that was made by user with `user_id`
    :param user_id: user which made some action
    :param log_type: action type e.g. update, create
    :param log_msg: action message e.g. item status has been changed to approved
    """
    try:
        user = User.objects.get(id=user_id)
        logger.info(f"User log for user {user.full_name} with type '{log_type}' and message '{log_msg}' was created")
    except User.DoesNotExist as e:
        logger.error(e)
