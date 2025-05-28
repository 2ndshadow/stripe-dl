# Stripe Invoice Downloader

Скрипт `download_invoices.py` автоматически сохраняет PDF‑инвойсы по списку **Invoice / Charge / PaymentIntent** ID. Подходит для macOS, Linux и Windows.

---

## 1. Что делает скрипт

* Читает файл `invoice_ids.csv` (по одному ID в строке). Поддерживаются:
  * `in_…` — Invoice ID
  * `ch_…`, `py_…` — Charge ID
  * `pi_…` — PaymentIntent ID
* Для каждого ID определяет, где лежит счёт, и скачивает `invoice_pdf`.
* Сохраняет файлы в папку **`invoices/`** как `in_XXXXXXXX.pdf`.

---

## 2. Требования

* **Python 3.8+**
* Пакеты: `stripe`, `requests`, `python-dotenv`
* Stripe API‑ключ c правами **Invoices → Read, Charges → Read, Payment Intents → Read**.

---

## 3. Установка

```bash
# 1. Клонируйте репозиторий или положите скрипт в отдельную папку
cd ~/projects/stripe-dl

# 2. Создайте виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate

# 3. Установите зависимости
pip install stripe requests python-dotenv
```

---

## 4. Настройка

1. **API‑ключ**  
   В корне проекта создайте файл `.env`:

   ```env
   STRIPE_SECRET_KEY=rk_live_xxxxxxxxxxxxxxxxxxxx
   ```

   Ограничьте права ключа (Invoices/Charges/PaymentIntents → Read) и удаляйте после выгрузки.

2. **Список ID**  
   Файл `invoice_ids.csv`, формат:

   ```
   ch_3RJtDGBkBGkwtT0Q1VZTeGkO
   in_1P9abcDefGhijKLmn
   pi_3RK4…
   ```

---

## 5. Запуск

```bash
source .venv/bin/activate      # если окружение ещё не активно
python download_invoices.py    # PDF‑ы появятся в ./invoices/
```

Прогресс выводится в консоль: ✔ — сохранено, ⚠️ — счёт не найден, ❌ — ошибка.

---

## 6. Автоматизация (cron/launchd)

Пример cron‑задания (2‑го числа каждого месяца в 06:00):

```cron
0 6 2 * *  cd /Users/you/projects/stripe-dl && source .venv/bin/activate && python download_invoices.py >> cron.log 2>&1
```

1. **Создать/вставить ключ** перед запуском.  
2. **Удалить/отозвать ключ** после выгрузки.

---

## 7. FAQ

| Вопрос | Ответ |
|--------|-------|
| Скрипт пишет «платёж без invoice» | Платёж имеет только чек (`receipt_url`) — счёт не создавался. |
| Как скачать receipts? | Дополнить скрипт: брать `receipt_url` и конвертировать в PDF headless‑браузером. |
| Что с Search API? | Не используется. Связь Charge ⇄ Invoice определяется через Invoice Payment API (2025‑03‑31+) или `payment_intent.invoice`. |

---

## 8. Обновление Stripe API‑версии

Скрипт совместим с версиями **до** 2025‑03‑31 и новее.  
Для поддержки будущих изменений обновляйте пакет `stripe`:

```bash
pip install --upgrade stripe
```

---

MIT License © 2025 Subsquid Labs GmbH
