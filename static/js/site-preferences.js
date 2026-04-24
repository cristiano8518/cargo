(function() {
  function getLang() {
    var htmlLang = (document.documentElement.getAttribute("lang") || "kk").toLowerCase();
    return htmlLang.slice(0, 2);
  }

  function applyTheme(theme) {
    var t = theme === "dark" ? "dark" : "light";
    document.body.classList.toggle("theme-dark", t === "dark");
    document.documentElement.setAttribute("data-bs-theme", t);
    try { localStorage.setItem("cargo-theme", t); } catch (e) {}
  }

  function bootstrapTheme() {
    var theme = "light";
    try { theme = localStorage.getItem("cargo-theme") || "light"; } catch (e) {}
    applyTheme(theme);
  }

  function translateNodeText(node, map) {
    var text = node.nodeValue;
    if (!text) return;
    var trimmed = text.trim();
    if (!trimmed) return;
    var translated = map[trimmed];
    if (translated) {
      node.nodeValue = text.replace(trimmed, translated);
      return;
    }
    var replaced = replaceByDictionary(text, map);
    if (replaced !== text) node.nodeValue = replaced;
  }

  function translateAttributes(el, map) {
    ["placeholder", "title", "aria-label"].forEach(function(attr) {
      var v = el.getAttribute(attr);
      if (!v) return;
      var direct = map[v.trim()];
      if (direct) {
        el.setAttribute(attr, direct);
        return;
      }
      var replaced = replaceByDictionary(v, map);
      if (replaced !== v) el.setAttribute(attr, replaced);
    });
    if ((el.tagName === "INPUT" || el.tagName === "BUTTON") && el.type === "submit") {
      var value = el.getAttribute("value");
      if (value && map[value.trim()]) el.setAttribute("value", map[value.trim()]);
    }
  }

  function escapeRegExp(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function replaceByDictionary(text, map) {
    var keys = Object.keys(map || {}).sort(function(a, b) { return b.length - a.length; });
    var out = text;
    keys.forEach(function(k) {
      if (!k || out.indexOf(k) === -1) return;
      var re = new RegExp(escapeRegExp(k), "g");
      out = out.replace(re, map[k]);
    });
    return out;
  }

  function walkAndTranslate(root, map) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function(n) { translateNodeText(n, map); });
    root.querySelectorAll("*").forEach(function(el) { translateAttributes(el, map); });
  }

  function translateSelectOptions(map) {
    document.querySelectorAll("option").forEach(function(opt) {
      var text = (opt.textContent || "").trim();
      if (!text) return;
      if (map[text]) opt.textContent = map[text];
    });
  }

  function enhanceFileInputs(lang, map) {
    document.querySelectorAll('input[type="file"]').forEach(function(input) {
      if (input.dataset.enhanced === "1") return;
      input.dataset.enhanced = "1";
      input.classList.add("visually-hidden");

      var wrap = document.createElement("div");
      wrap.className = "d-flex align-items-center gap-2 flex-wrap mt-1";
      input.parentNode.insertBefore(wrap, input.nextSibling);
      wrap.appendChild(input);

      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "btn btn-sm btn-outline-secondary";
      btn.textContent = lang === "ru" ? "Выбрать файл" : (lang === "en" ? "Choose file" : "Файл таңдау");
      btn.addEventListener("click", function() { input.click(); });
      wrap.appendChild(btn);

      var status = document.createElement("span");
      status.className = "small text-muted";
      status.textContent = map["Файл не выбран."] || (lang === "ru" ? "Файл не выбран." : (lang === "en" ? "No file selected." : "Файл таңдалмаған."));
      wrap.appendChild(status);

      input.addEventListener("change", function() {
        status.textContent = input.files && input.files[0] ? input.files[0].name : (map["Файл не выбран."] || status.textContent);
      });
    });
  }

  function applyDataI18n(root, map) {
    root.querySelectorAll("[data-i18n]").forEach(function(el) {
      var key = el.getAttribute("data-i18n");
      if (key && map[key]) el.textContent = map[key];
    });
    root.querySelectorAll("[data-i18n-html]").forEach(function(el) {
      var key = el.getAttribute("data-i18n-html");
      if (key && map[key]) el.innerHTML = map[key];
    });
  }

  function startLiveTranslation(map, lang) {
    if (!map || lang === "kk") return;
    var observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(m) {
        if (m.type === "childList") {
          m.addedNodes.forEach(function(node) {
            if (!node) return;
            if (node.nodeType === Node.TEXT_NODE) {
              translateNodeText(node, map);
              return;
            }
            if (node.nodeType === Node.ELEMENT_NODE) {
              walkAndTranslate(node, map);
              applyDataI18n(node, map);
              translateSelectOptions(map);
              enhanceFileInputs(lang, map);
            }
          });
        } else if (m.type === "characterData" && m.target) {
          translateNodeText(m.target, map);
        }
      });
    });
    observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true
    });
  }

  var dictionaries = {
    ru: {
      "Профиль": "Профиль",
      "Құпиясөзді өзгерту": "Сменить пароль",
      "Профильді жаңарту": "Обновить профиль",
      "Сақтау": "Сохранить",
      "Толық ақпарат": "Подробная информация",
      "Логин:": "Логин:",
      "Рөл:": "Роль:",
      "Қайда жұмыс істейді:": "Место работы:",
      "Қайда оқиды:": "Место учебы:",
      "Өзі туралы:": "О себе:",
      "Баптаулар": "Настройки",
      "Тақырып": "Тема",
      "Жарық": "Светлая",
      "Қараңғы": "Тёмная",
      "Тіл": "Язык",
      "Нұсқаулық кітапша": "Книга-руководство",
      "Тапсырыс беру": "Оформить заказ",
      "Тіркелу": "Регистрация",
      "Кіру": "Вход",
      "Ашу": "Открыть",
      "Жаңа тапсырыс": "Новый заказ",
      "Барлық тапсырыстар": "Все заказы",
      "Төлем жасаңыз (оплата):": "Выполните оплату:",
      "Тауарларыңыз келді:": "Ваши товары доставлены:",
      "Көрдім": "Понял",
      "Тапсырыстар саны": "Количество заказов",
      "Жалпы баға": "Общая сумма",
      "Статус бойынша": "По статусам",
      "Соңғы тапсырыстар": "Последние заказы",
      "Әзірге тапсырыс жоқ.": "Пока нет заказов.",
      "Менің тапсырыстарым": "Мои заказы",
      "Қолдану": "Применить",
      "Маршрут": "Маршрут",
      "Жүк": "Груз",
      "Баға": "Цена",
      "Статус": "Статус",
      "Көру": "Открыть",
      "Тапсырыс жоқ.": "Заказов нет.",
      "Алдыңғы": "Назад",
      "Келесі": "Вперёд",
      "Маршруттар": "Маршруты",
      "Админда басқару": "Управление в админке",
      "Карта": "Карта",
      "Маршрут құру": "Построить маршрут",
      "Жаңа тапсырысқа қосу": "Добавить в новый заказ",
      "Тағы бастау": "Начать заново",
      "Іздеу": "Поиск",
      "Картада көрсету": "Показать на карте",
      "Маршрут табылмады. Админ панельден қосып көріңіз.": "Маршруты не найдены. Добавьте их в админ-панели.",
      "Жүк түрлері": "Типы груза",
      "Тапсырысқа қосу": "Добавить в заказ",
      "Жүк түрі табылмады. Админ панельден қосып көріңіз.": "Типы груза не найдены. Добавьте их в админ-панели.",
      "Аккаунтыңыз бар ма?": "У вас уже есть аккаунт?",
      "Аккаунтыңыз жоқ па?": "Нет аккаунта?",
      "Карго жеткізу": "Cargo доставка",
      "Тапсырыстарыңызды басқарыңыз, статусты қадағалаңыз және төлем жасаңыз.": "Управляйте заказами, отслеживайте статус и оплачивайте.",
      "Логин немесе құпиясөз қате. Қайта тексеріп, тағы кіріп көріңіз.": "Неверный логин или пароль. Проверьте и попробуйте снова.",
      "Логин": "Логин",
      "Құпиясөз": "Пароль"
      ,"Жаңа тапсырыс": "Новый заказ"
      ,"Тапсырысты өңдеу": "Редактировать заказ"
      ,"Тек тізімнен таңдаңыз: жүк түрі (мал немесе тауар), маршрут (қайдан → қайда), салмақ, көлік түрі, жеткізу күні.": "Выбирайте только из списка: тип груза, маршрут, вес, тип транспорта, дата доставки."
      ,"Маршрут (картадан):": "Маршрут (с карты):"
      ,"Болдырмау": "Отмена"
      ,"Өшіру": "Удалить"
      ,"Кері байланыс": "Обратная связь"
      ,"Пікір қалдыру": "Оставить отзыв"
      ,"Жіберу": "Отправить"
      ,"Менің пікірлерім": "Мои отзывы"
      ,"Тапсырыс": "Заказ"
      ,"Әкімші жауабы:": "Ответ администратора:"
      ,"Әзірге пікір жоқ.": "Пока отзывов нет."
      ,"Барлық пайдаланушылардың пікірлері": "Отзывы всех пользователей"
      ,"Әзірге жария пікірлер жоқ.": "Пока нет публичных отзывов."
      ,"Қабылдау": "Принять"
      ,"Қабылдамау": "Отклонить"
      ,"Қабылдамау себебі": "Причина отклонения"
      ,"Байланыс": "Контакты"
      ,"Сұрақтарға жауап алу үшін бізбен байланысыңыз": "Свяжитесь с нами, чтобы получить ответы на вопросы"
      ,"Телефон (басты филиал)": "Телефон (главный филиал)"
      ,"Хабарлама жіберу": "Отправить сообщение"
      ,"Пікірлер панелі": "Панель отзывов"
      ,"Әзірге пікірлер жоқ. Алғашқы пікірді сіз қалдырыңыз!": "Пока отзывов нет. Оставьте первый отзыв!"
      ,"Біздің мекенжайлар": "Наши адреса"
      ,"Қазақстанның 5 қаласында — Алматы (басты филиал), Шымкент, Атырау, Қарағанды, Тараз": "В 5 городах Казахстана — Алматы (главный филиал), Шымкент, Атырау, Караганда, Тараз"
      ,"Басты филиал": "Главный филиал"
      ,"Мекенжайлар:": "Адреса:"
      ,"Тапсырысты өшіру": "Удаление заказа"
      ,"Иә, өшіру": "Да, удалить"
      ,"Фото": "Фото"
      ,"Профильді жаңарту": "Обновление профиля"
      ,"Қазіргі фото жоғарыда көрсетілген. Жаңасын таңдасаңыз алмастырылады.": "Текущее фото показано выше. При выборе нового оно будет заменено."
      ,"Маршруттар": "Маршруты"
      ,"Кестеден маршрутты таңдап «Картада көрсету» басыңыз — немесе «Маршрут құру» басып картада екі нүктені таңдаңыз.": "Выберите маршрут из таблицы и нажмите «Показать на карте» — или нажмите «Построить маршрут» и выберите две точки на карте."
      ,"Қашықтық:": "Расстояние:"
      ,"Шамалы баға:": "Ориентировочная цена:"
      ,"Осы маршрутпен тапсырыс беру": "Оформить заказ по этому маршруту"
      ,"Іздеу (шығу/келу)": "Поиск (откуда/куда)"
      ,"Шыққан жер": "Пункт отправления"
      ,"Келу жер": "Пункт прибытия"
      ,"Қашықтық": "Расстояние"
      ,"Картада көрсету": "Показать на карте"
      ,"Маршрут табылмады. Админ панельден қосып көріңіз.": "Маршрут не найден. Добавьте его в админ-панели."
      ,"Тапсырыс #": "Заказ #"
      ,"Өңдеу": "Редактировать"
      ,"Тапсырысыңыз қабылданды": "Ваш заказ принят"
      ,"Төлем сомасы:": "Сумма оплаты:"
      ,"Төлем жасау": "Оплатить"
      ,"Басканда статус «Төленді» болып, содан кейін «Жолда» жаңарады.": "После нажатия статус станет «Оплачено», затем обновится на «В пути»."
      ,"Жүк түрі:": "Тип груза:"
      ,"Салмақ:": "Вес:"
      ,"Көлік түрі:": "Тип транспорта:"
      ,"Есептелген баға:": "Расчётная стоимость:"
      ,"Не тасымалдау:": "Что перевозить:"
      ,"Қайдан:": "Откуда:"
      ,"Қайда жеткізу:": "Куда доставить:"
      ,"Жеткізу күні:": "Дата доставки:"
      ,"Қабылдамау себебі:": "Причина отказа:"
      ,"Құрылды:": "Создан:"
      ,"Жеткізу фотосы": "Фото доставки"
      ,"Жеткізу фото": "Фото доставки"
      ,"Бұл фото әкімші тапсырысты «Жеткізілді» деп жаңартқан кезде тіркелді.": "Это фото загружено администратором при установке статуса «Доставлено»."
      ,"Тауар жеткізілгенін растайтын фото": "Фото подтверждения доставки товара"
      ,"Маршрут картада": "Маршрут на карте"
      ,"Сіз қалдырған пікірлер": "Ваши отзывы"
      ,"Тізімге қайту": "Вернуться к списку"
      ,"Қате": "Ошибка"
      ,"Карта жүктелу қатесі.": "Ошибка загрузки карты."
      ,"Жол жүктелу қатесі.": "Ошибка загрузки маршрута."
      ,"Жүктелуде…": "Загрузка…"
      ,"Шығу": "Отправление"
      ,"Келу": "Прибытие"
      ,"Admin — Тапсырыстар": "Админ — Заказы"
      ,"Admin: барлық тапсырыстар": "Админ: все заказы"
      ,"Іздеу: user / сипаттама / маршрут": "Поиск: user / описание / маршрут"
      ,"Статус (бәрі)": "Статус (все)"
      ,"Көлік": "Транспорт"
      ,"Күні": "Дата"
      ,"Қабылдау/Қабылдамау": "Принять/Отклонить"
      ,"Себеп:": "Причина:"
      ,"Жабу": "Закрыть"
      ,"Тапсырысты өңдеу": "Редактирование заказа"
      ,"Тек тізімнен таңдаңыз: жүк түрі (мал немесе тауар), маршрут (қайдан → қайда), салмақ, көлік түрі, жеткізу күні.": "Выбирайте только из списка: тип груза (животные или товар), маршрут (откуда → куда), вес, тип транспорта, дата доставки."
      ,"Маршрут (картадан):": "Маршрут (с карты):"
      ,"Басқа": "Другое"
      ,"Кері байланыстар": "Отзывы"
      ,"Admin: Кері байланыстар": "Админ: Отзывы"
      ,"Іздеу: user / мәтін / тапсырыс #": "Поиск: user / текст / заказ #"
      ,"Мәтін": "Текст"
      ,"Жауап": "Ответ"
      ,"Жауап...": "Ответ..."
      ,"Кері байланыс жоқ.": "Отзывов нет."
      ,"Қабылдау/Қабылдамау — #": "Принять/Отклонить — #"
      ,"Тапсырыс #": "Заказ #"
      ,"Тапсырыс #{{ order.id }} — қабылдау немесе қабылдамау": "Заказ #{{ order.id }} — принять или отклонить"
      ,"Пайдаланушы:": "Пользователь:"
      ,"Көлік:": "Транспорт:"
      ,"Сипаттама:": "Описание:"
      ,"Қайда:": "Куда:"
      ,"Төлем сомасы (тг)": "Сумма оплаты (тг)"
      ,"Қабылдағанда пайдаланушыға жіберіледі": "При принятии будет отправлено пользователю"
      ,"Мысалы: көліктер бос емес, маршрут толық емес...": "Например: нет свободного транспорта, неполный маршрут..."
      ,"(міндетті)": "(обязательно)"
      ,"Байланыс — Карго": "Контакты — Cargo"
      ,"Сұрақтарға жауап алу үшін бізбен байланысыңыз": "Свяжитесь с нами, чтобы получить ответы на вопросы"
      ,"Email": "Email"
      ,"Хабарлама жіберу": "Отправить сообщение"
      ,"Пікірлер панелі": "Панель отзывов"
      ,"Әзірге пікірлер жоқ. Алғашқы пікірді сіз қалдырыңыз!": "Пока отзывов нет. Оставьте первый отзыв!"
      ,"Біздің мекенжайлар — Карго": "Наши адреса — Cargo"
      ,"Қазақстанның 5 қаласында — Алматы (басты филиал), Шымкент, Атырау, Қарағанды, Тараз": "В 5 городах Казахстана — Алматы (главный филиал), Шымкент, Атырау, Караганда, Тараз"
      ,"Басты филиал": "Главный филиал"
      ,"Мекенжайлар:": "Адреса:"
      ,"Тапсырысты өшіру": "Удаление заказа"
      ,"Сіз расымен #{{ order.id }} тапсырысын өшіргіңіз келе ме?": "Вы действительно хотите удалить заказ #{{ order.id }}?"
      ,"Иә, өшіру": "Да, удалить"
      ,"Dashboard": "Панель"
      ,"Басқару панелі": "Панель управления"
      ,"Тапсырыстар": "Заказы"
      ,"Байерлік қызмет": "Сервис байеров"
      ,"Шығу": "Выход"
      ,"Маршрутты таңдаңыз немесе «Маршрут құру» басыңыз.": "Выберите маршрут или нажмите «Построить маршрут»."
      ,"Сұраныс жіберілді": "Запрос отправлен"
      ,"Қабылданды": "Принято"
      ,"Қабылданбады": "Отклонено"
      ,"Төлем күтілуде": "Ожидает оплаты"
      ,"Төленді": "Оплачено"
      ,"Жолда": "В пути"
      ,"Жеткізілді": "Доставлено"
      ,"Бас тартылды": "Отменено"
      ,"Тапсырыс (қаласаңыз):": "Заказ (необязательно):"
      ,"— Тапсырыс таңдау (қаласаңыз) —": "— Выбрать заказ (необязательно) —"
      ,"Баға (1–5 жұлдыз):": "Оценка (1–5 звезд):"
      ,"Отзыв мәтіні:": "Текст отзыва:"
      ,"Өз пікіріңізді жазыңыз...": "Напишите ваш отзыв..."
      ,"Фото (қаласаңыз):": "Фото (необязательно):"
      ,"Файл не выбран.": "Файл не выбран."
      ,"Аты": "Имя"
      ,"Тегі": "Фамилия"
      ,"Қайда жұмыс істейді": "Где работает"
      ,"Қайда оқиды": "Где учится"
      ,"Қысқаша өзі туралы": "Коротко о себе"
      ,"Картада алдымен шығу пунктіні, содан келу пунктіні басыңыз.": "Сначала нажмите точку отправления, затем точку прибытия на карте."
      ,"Енді келу пунктіні басыңыз.": "Теперь нажмите точку прибытия."
      ,"Қашықтық пен баға есептелді.": "Расстояние и цена рассчитаны."
      ,"Жүктелу қатесі.": "Ошибка загрузки."
      ,"Жылқы": "Лошадь"
      ,"Ешкі": "Коза"
      ,"Сиыр": "Корова"
      ,"Қой": "Овца"
      ,"Тауық": "Курица"
      ,"Балық": "Рыба"
      ,"Көкөніс": "Овощи"
      ,"Жеміс": "Фрукты"
      ,"Жиһаз": "Мебель"
      ,"Техника": "Техника"
    },
    en: {
      "Профиль": "Profile",
      "Құпиясөзді өзгерту": "Change password",
      "Профильді жаңарту": "Update profile",
      "Сақтау": "Save",
      "Толық ақпарат": "Detailed information",
      "Логин:": "Username:",
      "Рөл:": "Role:",
      "Қайда жұмыс істейді:": "Work place:",
      "Қайда оқиды:": "Study place:",
      "Өзі туралы:": "About:",
      "Баптаулар": "Settings",
      "Тақырып": "Theme",
      "Жарық": "Light",
      "Қараңғы": "Dark",
      "Тіл": "Language",
      "Нұсқаулық кітапша": "Guide book",
      "Тапсырыс беру": "Create order",
      "Тіркелу": "Sign up",
      "Кіру": "Login",
      "Ашу": "Open",
      "Жаңа тапсырыс": "New order",
      "Барлық тапсырыстар": "All orders",
      "Төлем жасаңыз (оплата):": "Complete payment:",
      "Тауарларыңыз келді:": "Your goods were delivered:",
      "Көрдім": "Seen",
      "Тапсырыстар саны": "Orders count",
      "Жалпы баға": "Total price",
      "Статус бойынша": "By status",
      "Соңғы тапсырыстар": "Recent orders",
      "Әзірге тапсырыс жоқ.": "No orders yet.",
      "Менің тапсырыстарым": "My orders",
      "Қолдану": "Apply",
      "Маршрут": "Route",
      "Жүк": "Cargo",
      "Баға": "Price",
      "Статус": "Status",
      "Көру": "View",
      "Тапсырыс жоқ.": "No orders.",
      "Алдыңғы": "Previous",
      "Келесі": "Next",
      "Маршруттар": "Routes",
      "Админда басқару": "Manage in admin",
      "Карта": "Map",
      "Маршрут құру": "Build route",
      "Жаңа тапсырысқа қосу": "Add to new order",
      "Тағы бастау": "Start again",
      "Іздеу": "Search",
      "Картада көрсету": "Show on map",
      "Маршрут табылмады. Админ панельден қосып көріңіз.": "No routes found. Add them in admin panel.",
      "Жүк түрлері": "Cargo types",
      "Тапсырысқа қосу": "Add to order",
      "Жүк түрі табылмады. Админ панельден қосып көріңіз.": "No cargo types found. Add them in admin panel.",
      "Аккаунтыңыз бар ма?": "Already have an account?",
      "Аккаунтыңыз жоқ па?": "No account yet?",
      "Карго жеткізу": "Cargo delivery",
      "Тапсырыстарыңызды басқарыңыз, статусты қадағалаңыз және төлем жасаңыз.": "Manage your orders, track statuses, and make payments.",
      "Логин немесе құпиясөз қате. Қайта тексеріп, тағы кіріп көріңіз.": "Invalid username or password. Please try again.",
      "Логин": "Username",
      "Құпиясөз": "Password"
      ,"Жаңа тапсырыс": "New order"
      ,"Тапсырысты өңдеу": "Edit order"
      ,"Тек тізімнен таңдаңыз: жүк түрі (мал немесе тауар), маршрут (қайдан → қайда), салмақ, көлік түрі, жеткізу күні.": "Choose only from the list: cargo type, route, weight, vehicle type, delivery date."
      ,"Маршрут (картадан):": "Route (from map):"
      ,"Болдырмау": "Cancel"
      ,"Өшіру": "Delete"
      ,"Кері байланыс": "Feedback"
      ,"Пікір қалдыру": "Leave feedback"
      ,"Жіберу": "Send"
      ,"Менің пікірлерім": "My feedbacks"
      ,"Тапсырыс": "Order"
      ,"Әкімші жауабы:": "Admin reply:"
      ,"Әзірге пікір жоқ.": "No feedback yet."
      ,"Барлық пайдаланушылардың пікірлері": "Feedback from all users"
      ,"Әзірге жария пікірлер жоқ.": "No public feedback yet."
      ,"Қабылдау": "Approve"
      ,"Қабылдамау": "Reject"
      ,"Қабылдамау себебі": "Rejection reason"
      ,"Байланыс": "Contact"
      ,"Сұрақтарға жауап алу үшін бізбен байланысыңыз": "Contact us to get answers to your questions"
      ,"Телефон (басты филиал)": "Phone (main branch)"
      ,"Хабарлама жіберу": "Send message"
      ,"Пікірлер панелі": "Reviews panel"
      ,"Әзірге пікірлер жоқ. Алғашқы пікірді сіз қалдырыңыз!": "No reviews yet. Be the first to leave one!"
      ,"Біздің мекенжайлар": "Our addresses"
      ,"Қазақстанның 5 қаласында — Алматы (басты филиал), Шымкент, Атырау, Қарағанды, Тараз": "In 5 cities of Kazakhstan — Almaty (main branch), Shymkent, Atyrau, Karaganda, Taraz"
      ,"Басты филиал": "Main branch"
      ,"Мекенжайлар:": "Addresses:"
      ,"Тапсырысты өшіру": "Delete order"
      ,"Иә, өшіру": "Yes, delete"
      ,"Фото": "Photo"
      ,"Профильді жаңарту": "Profile update"
      ,"Қазіргі фото жоғарыда көрсетілген. Жаңасын таңдасаңыз алмастырылады.": "Current photo is shown above. Choosing a new one will replace it."
      ,"Кестеден маршрутты таңдап «Картада көрсету» басыңыз — немесе «Маршрут құру» басып картада екі нүктені таңдаңыз.": "Select a route from the table and click 'Show on map' — or click 'Build route' and pick two points on the map."
      ,"Қашықтық:": "Distance:"
      ,"Шамалы баға:": "Estimated price:"
      ,"Осы маршрутпен тапсырыс беру": "Create order with this route"
      ,"Іздеу (шығу/келу)": "Search (origin/destination)"
      ,"Шыққан жер": "Origin"
      ,"Келу жер": "Destination"
      ,"Қашықтық": "Distance"
      ,"Маршрут табылмады. Админ панельден қосып көріңіз.": "No route found. Add it via admin panel."
      ,"Өңдеу": "Edit"
      ,"Тапсырысыңыз қабылданды": "Your order has been accepted"
      ,"Төлем сомасы:": "Payment amount:"
      ,"Төлем жасау": "Pay now"
      ,"Басканда статус «Төленді» болып, содан кейін «Жолда» жаңарады.": "After clicking, status becomes 'Paid', then updates to 'In transit'."
      ,"Жүк түрі:": "Cargo type:"
      ,"Салмақ:": "Weight:"
      ,"Көлік түрі:": "Vehicle type:"
      ,"Есептелген баға:": "Estimated price:"
      ,"Не тасымалдау:": "Description:"
      ,"Қайдан:": "From:"
      ,"Қайда жеткізу:": "To:"
      ,"Жеткізу күні:": "Delivery date:"
      ,"Қабылдамау себебі:": "Rejection reason:"
      ,"Құрылды:": "Created:"
      ,"Жеткізу фотосы": "Delivery photo"
      ,"Жеткізу фото": "Delivery photo"
      ,"Бұл фото әкімші тапсырысты «Жеткізілді» деп жаңартқан кезде тіркелді.": "This photo is attached by admin when order is marked as delivered."
      ,"Тауар жеткізілгенін растайтын фото": "Delivery confirmation photo"
      ,"Маршрут картада": "Route on map"
      ,"Сіз қалдырған пікірлер": "Your feedback"
      ,"Тізімге қайту": "Back to list"
      ,"Қате": "Error"
      ,"Карта жүктелу қатесі.": "Map loading error."
      ,"Жол жүктелу қатесі.": "Route loading error."
      ,"Жүктелуде…": "Loading…"
      ,"Шығу": "Start"
      ,"Келу": "Arrival"
      ,"Admin: барлық тапсырыстар": "Admin: all orders"
      ,"Іздеу: user / сипаттама / маршрут": "Search: user / description / route"
      ,"Статус (бәрі)": "Status (all)"
      ,"Көлік": "Vehicle"
      ,"Күні": "Date"
      ,"Қабылдау/Қабылдамау": "Approve/Reject"
      ,"Себеп:": "Reason:"
      ,"Жабу": "Close"
      ,"Тек тізімнен таңдаңыз: жүк түрі (мал немесе тауар), маршрут (қайдан → қайда), салмақ, көлік түрі, жеткізу күні.": "Choose from list only: cargo type, route, weight, vehicle type, delivery date."
      ,"Маршрут (картадан):": "Route (from map):"
      ,"Басқа": "Other"
      ,"Кері байланыстар": "Feedback"
      ,"Admin: Кері байланыстар": "Admin: Feedback"
      ,"Іздеу: user / мәтін / тапсырыс #": "Search: user / text / order #"
      ,"Мәтін": "Text"
      ,"Жауап": "Reply"
      ,"Жауап...": "Reply..."
      ,"Кері байланыс жоқ.": "No feedback."
      ,"Тапсырыс #{{ order.id }} — қабылдау немесе қабылдамау": "Order #{{ order.id }} — approve or reject"
      ,"Пайдаланушы:": "User:"
      ,"Көлік:": "Vehicle:"
      ,"Сипаттама:": "Description:"
      ,"Қайда:": "To:"
      ,"Төлем сомасы (тг)": "Payment amount (KZT)"
      ,"Қабылдағанда пайдаланушыға жіберіледі": "Will be sent to user upon approval"
      ,"Мысалы: көліктер бос емес, маршрут толық емес...": "Example: no free vehicles, route incomplete..."
      ,"(міндетті)": "(required)"
      ,"Сұрақтарға жауап алу үшін бізбен байланысыңыз": "Contact us to get answers to your questions"
      ,"Біздің мекенжайлар — Карго": "Our addresses — Cargo"
      ,"Сіз расымен #{{ order.id }} тапсырысын өшіргіңіз келе ме?": "Are you sure you want to delete order #{{ order.id }}?"
      ,"Басқару панелі": "Dashboard"
      ,"Тапсырыстар": "Orders"
      ,"Байерлік қызмет": "Buyer service"
      ,"Шығу": "Logout"
      ,"Маршрутты таңдаңыз немесе «Маршрут құру» басыңыз.": "Choose a route or click 'Build route'."
      ,"Сұраныс жіберілді": "Request sent"
      ,"Қабылданды": "Accepted"
      ,"Қабылданбады": "Rejected"
      ,"Төлем күтілуде": "Payment pending"
      ,"Төленді": "Paid"
      ,"Жолда": "In transit"
      ,"Жеткізілді": "Delivered"
      ,"Бас тартылды": "Cancelled"
      ,"Тапсырыс (қаласаңыз):": "Order (optional):"
      ,"— Тапсырыс таңдау (қаласаңыз) —": "— Select order (optional) —"
      ,"Баға (1–5 жұлдыз):": "Rating (1–5 stars):"
      ,"Отзыв мәтіні:": "Review text:"
      ,"Өз пікіріңізді жазыңыз...": "Write your review..."
      ,"Фото (қаласаңыз):": "Photo (optional):"
      ,"Файл не выбран.": "No file selected."
      ,"Аты": "First name"
      ,"Тегі": "Last name"
      ,"Қайда жұмыс істейді": "Work place"
      ,"Қайда оқиды": "Study place"
      ,"Қысқаша өзі туралы": "Short bio"
      ,"Картада алдымен шығу пунктіні, содан келу пунктіні басыңыз.": "Click departure point first, then arrival point on the map."
      ,"Енді келу пунктіні басыңыз.": "Now click the arrival point."
      ,"Қашықтық пен баға есептелді.": "Distance and price calculated."
      ,"Жүктелу қатесі.": "Loading error."
      ,"Жылқы": "Horse"
      ,"Ешкі": "Goat"
      ,"Сиыр": "Cow"
      ,"Қой": "Sheep"
      ,"Тауық": "Chicken"
      ,"Балық": "Fish"
      ,"Көкөніс": "Vegetables"
      ,"Жеміс": "Fruits"
      ,"Жиһаз": "Furniture"
      ,"Техника": "Equipment"
    }
  };

  bootstrapTheme();
  var lang = getLang();
  var activeMap = dictionaries[lang] || {};
  window.__cargoI18n = {
    lang: lang,
    t: function(key) { return activeMap[key] || key; }
  };
  if (lang !== "kk" && dictionaries[lang]) {
    walkAndTranslate(document.body, activeMap);
    applyDataI18n(document.body, activeMap);
    translateSelectOptions(activeMap);
    enhanceFileInputs(lang, activeMap);
    startLiveTranslation(activeMap, lang);
  }

  document.addEventListener("click", function(e) {
    var btn = e.target.closest(".js-theme-btn");
    if (!btn) return;
    applyTheme(btn.getAttribute("data-theme"));
    document.querySelectorAll(".js-theme-btn").forEach(function(b) {
      var active = b.getAttribute("data-theme") === (btn.getAttribute("data-theme") === "dark" ? "dark" : "light");
      b.classList.toggle("btn-primary", active);
      b.classList.toggle("btn-outline-secondary", !active);
    });
  });

  document.addEventListener("DOMContentLoaded", function() {
    var current = (localStorage.getItem("cargo-theme") || "light");
    document.querySelectorAll(".js-theme-btn").forEach(function(b) {
      var active = b.getAttribute("data-theme") === (current === "dark" ? "dark" : "light");
      b.classList.toggle("btn-primary", active);
      b.classList.toggle("btn-outline-secondary", !active);
    });
  });
})();
