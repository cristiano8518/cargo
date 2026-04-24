from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import CommonPasswordValidator


class LocalizedCommonPasswordValidator(CommonPasswordValidator):
    """
    Keeps Django common-password protection, but returns localized message.
    """

    def validate(self, password, user=None):
        if password and password.lower().strip() in self.passwords:
            raise ValidationError(
                "Бұл құпиясөз тым қарапайым. Күрделірек құпиясөз таңдаңыз.",
                code="password_too_common",
            )
