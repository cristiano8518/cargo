# Карго жеткізу веб-сайты (Байерлік қызмет)

Django жобасы — барлық негізгі файлдар дайын. Тек ортаны іске қосу керек.

---

## Жоба құрылымы

```
cargo/
├── manage.py
├── requirements.txt
├── README.md
├── cargo_project/       # Басты конфигурация
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/               # Пайдаланушылар (тіркелу, кіру, рөлдер)
├── orders/              # Тапсырыстар
├── cargo/               # Жүк түрлері, маршруттар
├── templates/
└── static/
```

---

## Орнату (3 қадам)

Терминалды **c:\Users\user\cargo** папкасында ашыңыз.

### 1. Виртуалды орта және Django

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

(Егер `Activate.ps1` табылмаса: **CMD** ашып `venv\Scripts\activate.bat` орындаңыз.)

### 2. Дерекқор миграциясы

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 3. Админ құру және серверді іске қосу

```powershell
python manage.py createsuperuser
python manage.py runserver
```

Браузерде:

- Үй беті: **http://127.0.0.1:8000/**
- Админ: **http://127.0.0.1:8000/admin/**

---

## Қысқаша мүмкіндіктер

| Бөлім | Сипаттама |
|-------|-----------|
| **users** | Пайдаланушы моделі (рөл: user/admin), админ-панельде басқару |
| **orders** | Тапсырыс моделі (шыққан/келу, мәртебе), админда тізім |
| **cargo** | Жүк түрі, маршрут — админда басқару |
| **URL** | `/`, `/admin/`, `/users/profile/`, `/orders/`, `/cargo/types/`, `/cargo/routes/` |

Кейінгі қадамдар: тіркелу/кіру беттері, REST API, тестілеу, Docker, CI/CD — талаптар бойынша қосылады.
