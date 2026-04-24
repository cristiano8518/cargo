from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import translation

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
    return render(
        request,
        "users/profile.html",
        {
            "form": form,
            "language_choices": [("kk", "Қазақша"), ("ru", "Русский"), ("en", "English")],
        },
    )


@login_required
def set_language_preference(request):
    lang = (request.session.get("django_language") or "kk").strip().lower()
    if request.method == "POST":
        lang = (request.POST.get("language") or "kk").strip().lower()
        if lang not in {"kk", "ru", "en"}:
            lang = "kk"
        request.session["django_language"] = lang
        translation.activate(lang)
    next_url = request.POST.get("next") or reverse("users:profile")
    response = HttpResponseRedirect(next_url)
    response.set_cookie("django_language", lang, max_age=60 * 60 * 24 * 365)
    return response


@login_required
def guide(request):
    lang = translation.get_language() or "kk"
    lang = lang.split("-")[0]
    if lang not in {"kk", "ru", "en"}:
        lang = "kk"

    guide_content = {
        "kk": {
            "title": "Платформаны пайдалану нұсқаулығы",
            "intro": "Бұл нұсқаулық сайттың барлық негізгі бөлімдерін қалай қолдануды түсіндіреді.",
            "sections": [
                ("1. Тіркелу және кіру", "Алдымен тіркеліңіз, содан кейін логин мен құпиясөз арқылы жүйеге кіріңіз."),
                ("2. Жүк түрін таңдау", "«Жүк түрлері» бөлімінде қажет жүкті таңдап, «Тапсырысқа қосу» батырмасын басыңыз."),
                ("3. Маршрут құру", "«Маршруттар» бөлімінде дайын маршрутты таңдаңыз немесе картада өз маршрутыңызды құрыңыз."),
                ("4. Тапсырыс беру", "Тапсырыс формасын толтырып, жіберіңіз. Статус дашбордта және тапсырыс тізімінде көрінеді."),
                ("5. Әкімші шешімі және төлем", "Әкімші қабылдағаннан кейін төлем бөлімі ашылады. Төлем жасаған соң статус жаңарады."),
                ("6. Кері байланыс", "Жеткізілген тапсырыстар бойынша баға қойып, пікір қалдырыңыз."),
            ],
        },
        "ru": {
            "title": "Руководство по использованию платформы",
            "intro": "Это руководство объясняет, как пользоваться всеми основными разделами сайта.",
            "sections": [
                ("1. Регистрация и вход", "Сначала зарегистрируйтесь, затем войдите в систему по логину и паролю."),
                ("2. Выбор типа груза", "В разделе «Типы груза» выберите нужный вариант и нажмите «Добавить в заказ»."),
                ("3. Построение маршрута", "В разделе «Маршруты» выберите готовый маршрут или постройте свой на карте."),
                ("4. Оформление заказа", "Заполните форму заказа и отправьте. Статус будет виден в дашборде и списке заказов."),
                ("5. Решение администратора и оплата", "После подтверждения админом откроется оплата. После оплаты статус обновится."),
                ("6. Обратная связь", "Для доставленных заказов оставляйте оценку и отзыв."),
            ],
        },
        "en": {
            "title": "Platform User Guide",
            "intro": "This guide explains how to use all key sections of the website.",
            "sections": [
                ("1. Sign up and sign in", "Create an account first, then sign in using your username and password."),
                ("2. Choose cargo type", "In the Cargo Types section, select a cargo type and click Add to Order."),
                ("3. Build a route", "In the Routes section, choose an existing route or build your own route on the map."),
                ("4. Create an order", "Fill in the order form and submit it. You can track status in dashboard and orders list."),
                ("5. Admin decision and payment", "After admin approval, payment becomes available. Status updates after payment."),
                ("6. Feedback", "For delivered orders, leave a rating and a review."),
            ],
        },
    }

    content = guide_content[lang]
    return render(request, "users/guide.html", {"guide": content})
