from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()

# To change default parameter of 7 days for token reset
# search Django docs for password_reset_timeout_days