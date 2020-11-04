import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class _TokenGenFactory(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.email) + six.text_type(user.password) + six.text_type(timestamp) \
               + six.text_type(user.is_active)


TokenGenerator = _TokenGenFactory()


def create_token_url(relative_url, token):
    """
    Generate full URL based on relative url and token
    :param relative_url: relative url
    :param token: token
    :return: url
    """
    return f"{relative_url.strip('/')}?token={token}"
