from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import redirect, render

from .forms import SignUpForm, ProfileUpdateForm
from orders.models import Order

def signup(request):
    if request.user.is_authenticated:
        return redirect("users:dashboard")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("users:dashboard")
    else:
        form = SignUpForm()
    return render(request, "users/signup.html", {"form": form})


@login_required
def dashboard(request):
    qs = Order.objects.filter(user=request.user)
    total_orders = qs.count()
    by_status = {row["status"]: row["c"] for row in qs.values("status").annotate(c=Count("id"))}
    total_estimated = qs.aggregate(s=Sum("estimated_price")).get("s") or 0
    last_orders = qs.order_by("-created_at")[:5]
    delivered = qs.filter(
        status__in=[Order.Status.DELIVERED, Order.Status.REJECTED],
        admin_seen=False,
    ).order_by("-updated_at")[:5]
    payment_pending_orders = qs.filter(status=Order.Status.PAYMENT_PENDING).order_by("-created_at")
    return render(
        request,
        "users/dashboard.html",
        {
            "total_orders": total_orders,
            "by_status": by_status,
            "status_choices": Order.Status.choices,
            "total_estimated": total_estimated,
            "last_orders": last_orders,
            "delivered_orders": delivered,
            "payment_pending_orders": payment_pending_orders,
        },
    )


@login_required
def profile(request):
    """Пайдаланушы профилі — көрсету және жаңарту."""
    user = request.user
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users:profile")
    else:
        form = ProfileUpdateForm(instance=user)
    return render(request, "users/profile.html", {"form": form})
