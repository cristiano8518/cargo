from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderForm
from .models import Order
from users.permissions import is_admin_user


ALLOWED_SORTS = {
    "-created_at": "Жаңасы алдымен",
    "created_at": "Ескісі алдымен",
    "status": "Статус бойынша",
}


@login_required
def order_list(request):
    qs = Order.objects.filter(user=request.user)

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
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})


@login_required
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order: Order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request, "Тапсырыс құрылды.")
            return redirect("orders:detail", pk=order.pk)
    else:
        form = OrderForm()
    return render(request, "orders/order_form.html", {"form": form, "mode": "create"})


@login_required
def order_update(request, pk: int):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Тапсырыс жаңартылды.")
            return redirect("orders:detail", pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, "orders/order_form.html", {"form": form, "mode": "update", "order": order})


@login_required
def order_delete(request, pk: int):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if request.method == "POST":
        order.delete()
        messages.success(request, "Тапсырыс өшірілді.")
        return redirect("orders:list")
    return render(request, "orders/order_confirm_delete.html", {"order": order})


@user_passes_test(is_admin_user)
def admin_order_list(request):
    qs = Order.objects.select_related("user", "cargo_type").all()

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
            order.save()
            messages.success(request, f"Статус жаңартылды: {order.get_status_display()}")
        else:
            messages.error(request, "Қате статус.")
    return redirect("orders:admin_list")
