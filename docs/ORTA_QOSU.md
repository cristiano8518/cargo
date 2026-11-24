# Ортаны қосу мәселесі шешімі

## 1-нұсқа: CMD және .bat файлдар (ең оңай)

PowerShell орнына **Command Prompt (CMD)** қолданыңыз.

1. **setup.bat** файлын **қос түймен басып** ашыңыз (немесе оны CMD-да орындаңыз):
   ```
   setup.bat
   ```
   Ол:
   - venv құрады (жоқ болса),
   - ортаны іске қосады (activate.bat),
   - Django орнатады,
   - миграция жасайды,
   - админ пайдаланушысын сұрайды.

2. Кейін серверді іске қосу үшін **run.bat** қос түймемен ашыңыз (немесе CMD-да `run.bat`).

---

## 2-нұсқа: CMD-да қолмен

1. **Win + R** басып, `cmd` жазып, Enter.
2. Жоба папкасына өтіңіз:
   ```
   cd C:\Users\user\cargo
   ```
3. Виртуалды ортаны құрыңыз (жоқ болса):
   ```
   python -m venv venv
   ```
4. Ортаны **CMD-да** осылай қосыңыз (PowerShell емес!):
   ```
   venv\Scripts\activate.bat
   ```
   Сәтті болса, алдыңызда `(venv)` шығады.
5. Django орнатыңыз:
   ```
   pip install -r requirements.txt
   ```
6. Миграция және сервер:
   ```
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

---

## 3-нұсқа: PowerShell-да рұқсат беру

PowerShell-да **Activate.ps1** «орындалуына рұқсат жоқ» деген қате шықса:

1. PowerShell-ды **администратор ретінде** ашыңыз (оң түйме → «Администратор ретінде іске қосу»).
2. Мынаны орындаңыз:
   ```
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Сұрағанда **Y** (Иә) басыңыз.
3. Кейін жоба папкасына келіп қайта көріңіз:
   ```
   cd C:\Users\user\cargo
   .\venv\Scripts\Activate.ps1
   ```

---

## Қорытынды

- **Ең оңай:** **setup.bat** қос түймемен ашыңыз, содан кейін **run.bat** — орта қолмен қосылмайды, скрипт өзі істейді.
- Қате хабарламасын көшіріп жіберсеңіз, нақты шешім жаза аламын.
