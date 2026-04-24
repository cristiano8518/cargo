from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from cargo.models import CargoType, Route
from .forms import OrderForm, OrderAdminUpdateForm, FeedbackForm
from .models import Order, Feedback
from users.permissions import is_admin_user


ALLOWED_SORTS = {
    "-created_at": "Жаңасы алдымен",
    "created_at": "Ескісі алдымен",
    "status": "Статус бойынша",
}


@login_required
def order_list(request):
    qs = Order.objects.filter(user=request.user).select_related("route", "cargo_type")

    q = (request.GET.get("q") or "").strip()
    if q:
        qs = qs.filter(
            Q(description__icontains=q)
            | Q(origin__icontains=q)
            | Q(destination__icontains=q)
        )

    status = (request.GET.get("status") or "").strip()
    if status:
        qs = qs.filter(status=status)

    sort = request.GET.get("sort") or "-created_at"
    if sort not in ALLOWED_SORTS:
        sort = "-created_at"
    qs = qs.order_by(sort)

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "orders/order_list.html",
        {
            "page_obj": page_obj,
            "q": q,
            "status": status,
            "sort": sort,
            "sort_options": ALLOWED_SORTS,
            "status_options": Order.Status.choices,
        },
    )


@login_required
def order_detail(request, pk: int):
    qs = Order.objects.select_related("route", "cargo_type")
    if is_admin_user(request.user):
        order = get_object_or_404(qs, pk=pk)
        feedbacks = Feedback.objects.filter(order=order).order_by("-created_at")
    else:
        order = get_object_or_404(qs, pk=pk, user=request.user)
        feedbacks = Feedback.objects.filter(user=request.user, order=order).order_by("-created_at")
    return render(request, "orders/order_detail.html", {"order": order, "feedbacks": feedbacks})


@login_required
def order_create(request):
    custom_route = request.session.get("custom_route")
    if request.method == "POST":
        form = OrderForm(request.POST)
        if custom_route:
            form.fields["route"].required = False
        if form.is_valid():
            order: Order = form.save(commit=False)
            order.user = request.user
            order.status = Order.Status.PENDING
            if order.cargo_type and order.cargo_type.name == "Басқа":
                order.description = form.cleaned_data.get("custom_cargo_name") or ""
            elif order.cargo_type:
                order.description = order.cargo_type.name
            if custom_route:
                order.route = None
                order.origin = custom_route["origin"]
                order.destination = custom_route["destination"]
                if "custom_route" in request.session:
                    del request.session["custom_route"]
            elif order.route:
                order.origin = order.route.origin
                order.destination = order.route.destination
            order.save()
            messages.success(request, "Сұраныс жіберілді. Әкімші тексергенше күтіңіз.")
            return redirect("orders:detail", pk=order.pk)
    else:
        initial = {}
        route_id = request.GET.get("route")
        if route_id and not custom_route:
            try:
                route = Route.objects.get(pk=route_id)
                initial["route"] = route
            except (Route.DoesNotExist, ValueError):
                pass
        cargo_type_id = request.GET.get("cargo_type")
        if cargo_type_id:
            try:
                ct = CargoType.objects.get(pk=cargo_type_id)
                initial["cargo_type"] = ct
            except (CargoType.DoesNotExist, ValueError):
                pass
        form = OrderForm(initial=initial)
        if custom_route:
            form.fields["route"].required = False
    return render(request, "orders/order_form.html", {
        "form": form,
        "mode": "create",
        "custom_route": custom_route,
    })


@login_required
def order_update(request, pk: int):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.status != Order.Status.PENDING:
        messages.info(request, "Тек «Сұраныс жіберілді» кезінде өңдеуге болады.")
        return redirect("orders:detail", pk=order.pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            if order.cargo_type and order.cargo_type.name == "Басқа":
                order.description = form.cleaned_data.get("custom_cargo_name") or ""
            elif order.cargo_type:
                order.description = order.cargo_type.name
            if order.route:
                order.origin = order.route.origin
                order.destination = order.route.destination
            order.save()
            messages.success(request, "Тапсырыс жаңартылды.")
            return redirect("orders:detail", pk=order.pk)
    else:
        initial = {}
        if order.cargo_type and order.cargo_type.name == "Басқа" and order.description:
            initial["custom_cargo_name"] = order.description
        form = OrderForm(instance=order, initial=initial)
    return render(request, "orders/order_form.html", {"form": form, "mode": "update", "order": order})


@login_required
def order_delete(request, pk: int):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if request.method == "POST":
        order.delete()
        messages.success(request, "Тапсырыс өшірілді.")
        return redirect("orders:list")
    return render(request, "orders/order_confirm_delete.html", {"order": order})


@login_required
def order_confirm_payment(request, pk: int):
    """Пайдаланушы «Төлем жасау» басқанда: Төленді → Жолда."""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.status != Order.Status.PAYMENT_PENDING:
        messages.info(request, "Төлем тек «Төлем күтілуде» тапсырыстар үшін.")
        return redirect("orders:detail", pk=pk)
    if request.method == "POST":
        order.status = Order.Status.PAID
        order.save(update_fields=["status", "updated_at"])
        order.status = Order.Status.IN_TRANSIT
        order.save(update_fields=["status", "updated_at"])
        messages.success(request, "Төлем жасалды. Тапсырыс жолда.")
        return redirect("orders:detail", pk=pk)
    return redirect("orders:detail", pk=pk)


@user_passes_test(is_admin_user)
def admin_order_list(request):
    qs = Order.objects.select_related("user", "cargo_type", "route").all()

    q = (request.GET.get("q") or "").strip()
    if q:
        qs = qs.filter(
            Q(description__icontains=q)
            | Q(origin__icontains=q)
            | Q(destination__icontains=q)
            | Q(user__username__icontains=q)
        )

    status = (request.GET.get("status") or "").strip()
    if status:
        qs = qs.filter(status=status)

    sort = request.GET.get("sort") or "-created_at"
    if sort not in ALLOWED_SORTS:
        sort = "-created_at"
    qs = qs.order_by(sort)

    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "orders/admin_order_list.html",
        {
            "page_obj": page_obj,
            "q": q,
            "status": status,
            "sort": sort,
            "sort_options": ALLOWED_SORTS,
            "status_options": Order.Status.choices,
        },
    )


@user_passes_test(is_admin_user)
def admin_order_set_status(request, pk: int):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("status") or ""
        valid = {v for v, _ in Order.Status.choices}
        if new_status in valid:
            order.status = new_status
            if new_status == Order.Status.DELIVERED:
                photo = request.FILES.get("delivery_photo")
                if photo:
                    order.delivery_photo = photo
            order.save()
            messages.success(request, f"Статус жаңартылды: {order.get_status_display()}")
        else:
            messages.error(request, "Қате статус.")
    return redirect("orders:admin_list")


@login_required
def order_mark_seen(request, pk: int):
    """Пайдаланушы: жеткізілген/қабылданбаған тапсырысты хабарламадан алып тастау."""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if request.method == "POST" and order.status in (Order.Status.DELIVERED, Order.Status.REJECTED):
        order.admin_seen = True
        order.save(update_fields=["admin_seen"])
    return redirect("users:dashboard")


@login_required
def feedback_list(request):
    """Пайдаланушының кері байланыс беті."""
    if request.user.is_staff or getattr(request.user, "role", "") == "admin" or request.user.is_superuser:
        return redirect("orders:admin_feedback")
    if request.method == "POST":
        form = FeedbackForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            fb: Feedback = form.save(commit=False)
            fb.user = request.user
            fb.save()
            messages.success(request, "Пікіріңіз үшін рақмет!")
            return redirect("orders:feedback")
    else:
        form = FeedbackForm(user=request.user)
    feedbacks = Feedback.objects.filter(user=request.user).select_related("order").order_by("-created_at")
    public_feedbacks = Feedback.objects.select_related("user", "order").exclude(user=request.user).order_by("-created_at")[:30]
    return render(
        request,
        "orders/feedback.html",
        {
            "form": form,
            "feedbacks": feedbacks,
            "public_feedbacks": public_feedbacks,
        },
    )


@user_passes_test(is_admin_user)
def admin_feedback_list(request):
    """Әкімші: барлық кері байланыстар және жауап беру."""
    qs = Feedback.objects.select_related("user", "order").all()
    q = (request.GET.get("q") or "").strip()
    if q:
        qs = qs.filter(
            Q(text__icontains=q)
            | Q(user__username__icontains=q)
            | Q(order__id__icontains=q)
        )
    feedbacks = qs.order_by("-created_at")

    if request.method == "POST":
        delete_id = request.POST.get("delete_id")
        if delete_id:
            fb = get_object_or_404(Feedback, pk=delete_id)
            fb.delete()
            messages.success(request, "Кері байланыс өшірілді.")
            return redirect("orders:admin_feedback")
        fb_id = request.POST.get("feedback_id")
        reply = (request.POST.get("admin_reply") or "").strip()
        if fb_id and reply:
            fb = get_object_or_404(Feedback, pk=fb_id)
            fb.admin_reply = reply
            fb.save(update_fields=["admin_reply", "updated_at"])
            messages.success(request, "Жауап сақталды.")
            return redirect("orders:admin_feedback")

    return render(request, "orders/admin_feedback_list.html", {"feedbacks": feedbacks, "q": q})


@user_passes_test(is_admin_user)
def admin_order_decision(request, pk: int):
    """Әкімші: қабылдау немесе қабылдамау — екі батырма, қабылданса төлем күтілуде."""
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        if request.POST.get("accept"):
            # Қабылдау — бағаны қойып, төлем күтілуде етіп жібереміз (пайдаланушыға оплата келеді)
            price = request.POST.get("estimated_price")
            try:
                order.estimated_price = float(price or 0)
            except (TypeError, ValueError):
                order.estimated_price = 0
            order.status = Order.Status.PAYMENT_PENDING
            order.rejection_reason = ""
            order.save()
            messages.success(request, "Сұраныс қабылданды. Пайдаланушыға төлем жіберілді.")
            return redirect("orders:admin_list")
        if request.POST.get("reject"):
            reason = (request.POST.get("rejection_reason") or "").strip()
            if not reason:
                messages.error(request, "Қабылдамау себебін жазыңыз.")
                return render(
                    request,
                    "orders/admin_order_decision.html",
                    {"order": order, "rejection_reason": reason},
                )
            order.status = Order.Status.REJECTED
            order.rejection_reason = reason
            order.save()
            messages.success(request, "Сұраныс қабылданбады.")
            return redirect("orders:admin_list")
    return render(
        request,
        "orders/admin_order_decision.html",
        {"order": order},
    )
