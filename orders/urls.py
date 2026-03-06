from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.order_list, name="list"),
    path("admin/", views.admin_order_list, name="admin_list"),
    path("admin/<int:pk>/status/", views.admin_order_set_status, name="admin_set_status"),
    path("admin/<int:pk>/decision/", views.admin_order_decision, name="admin_decision"),
    path("admin/feedback/", views.admin_feedback_list, name="admin_feedback"),
    path("new/", views.order_create, name="create"),
    path("<int:pk>/", views.order_detail, name="detail"),
    path("<int:pk>/pay/", views.order_confirm_payment, name="confirm_payment"),
    path("<int:pk>/edit/", views.order_update, name="update"),
    path("<int:pk>/delete/", views.order_delete, name="delete"),
    path("<int:pk>/seen/", views.order_mark_seen, name="mark_seen"),
    path("feedback/", views.feedback_list, name="feedback"),
]
