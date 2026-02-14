from rest_framework.permissions import BasePermission


def is_admin_user(user) -> bool:
    if not user or not getattr(user, "is_authenticated", False):
        return False
    return bool(getattr(user, "is_superuser", False) or getattr(user, "is_staff", False) or getattr(user, "role", "") == "admin")


class IsAdminRole(BasePermission):
    """
    Рөлге негізделген рұқсат: role=admin (немесе is_staff/is_superuser).
    """

    message = "Бұл әрекет тек әкімшіге рұқсат."

    def has_permission(self, request, view):
        return is_admin_user(getattr(request, "user", None))

