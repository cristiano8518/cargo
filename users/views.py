from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import redirect, render

from .forms import SignUpForm
from orders.models import Order

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("users:profile")
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
    return render(
        request,
        "users/dashboard.html",
        {
            "total_orders": total_orders,
            "by_status": by_status,
            "status_choices": Order.Status.choices,
            "total_estimated": total_estimated,
            "last_orders": last_orders,
        },
    )


@login_required
def profile(request):
    """Пайдаланушы профилі."""
    return render(request, "users/profile.html")
