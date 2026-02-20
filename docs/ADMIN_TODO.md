# Админка — толық тәртіпке келтіру тізімі

## 1. Order (Тапсырыстар) ✅
- [x] **Fieldsets** — Негізгі, Маршрут, Статус, Уақыт (collapse)
- [x] **readonly_fields** — created_at, updated_at
- [x] **list_per_page** — 20
- [x] **date_hierarchy** — created_at
- [x] **search_fields** — user__username, origin, destination, description, rejection_reason
- [x] **list_filter** — status, vehicle_type
- [x] **Admin actions** — Статусты: Сұраныс жіберілді / Төлем күтілуде / Жолда / Жеткізілді

## 2. User (Пайдаланушылар) ✅
- [x] **search_fields** — username, email, phone, first_name, last_name
- [x] **list_per_page** — 25
- [x] **ordering** — username
- [x] **list_display** — date_joined қосылды; list_filter — is_active

## 3. CargoType (Жүк түрлері) ✅
- [x] **ordering** — category, name
- [x] **list_per_page** — 25
- [x] **list_display** — description_short (қысқаша сипаттама)

## 4. Route (Маршруттар) ✅
- [x] **ordering** — origin, destination
- [x] **list_per_page** — 25

## 5. Жалпы
- [ ] Бос тізім хабарламы — Django әдепкі немесе LANGUAGE_CODE=kk жеткілікті

Барлығы орындалды.
