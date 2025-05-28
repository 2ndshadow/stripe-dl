#!/usr/bin/env python3
"""
download_invoices.py   (Stripe API ≥ 2025-03-31)
Читает ID из invoice_ids.csv (in_, ch_, py_, pi_) и сохраняет PDF-инвойсы в ./invoices/.
"""

import os, pathlib, time, requests, stripe
from dotenv import load_dotenv
from stripe.error import InvalidRequestError

# ────── конфигурация ──────
INPUT_FILE   = pathlib.Path("invoice_ids.csv")
OUTPUT_DIR   = pathlib.Path("invoices")
RATE_LIMIT_S = 0.02                               # 50 req/сек < лимита 100

# ────── Stripe key ──────
load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY") or exit("Нет STRIPE_SECRET_KEY")

# ────── util ──────
def read_ids(fp):       return [l.strip() for l in fp.read_text().splitlines() if l.strip()]

def save_pdf(url, stem):
    out = OUTPUT_DIR / f"{stem}.pdf";  OUTPUT_DIR.mkdir(exist_ok=True)
    r = requests.get(url, timeout=30); r.raise_for_status()
    out.write_bytes(r.content);  print(f"✔  {out.name}")

def download_invoice(inv_id):
    pdf = stripe.Invoice.retrieve(inv_id).get("invoice_pdf")
    if pdf: save_pdf(pdf, inv_id)
    else : print(f"⚠️  {inv_id}: invoice_pdf не найден")

# ────── новый поиск счёта через InvoicePayment ──────
def invoice_from_payment(charge_id=None, pi_id=None):
    try:
        if charge_id:
            resp = stripe.InvoicePayment.list(
                payment={"type": "charge", "charge": charge_id}, limit=1)
        else:
            resp = stripe.InvoicePayment.list(
                payment={"type": "payment_intent", "payment_intent": pi_id}, limit=1)
        data = resp["data"]
        if data:  return data[0]["invoice"]     # in_***
    except InvalidRequestError as e:
        # метод доступен только на API 2025-03-31+; для старых версий вернёт 400/404
        pass
    return None

# ────── главный цикл ──────
def main():
    ids = read_ids(INPUT_FILE)
    print(f"Найдено {len(ids)} ID — начинаю загрузку…\n")

    for raw in ids:
        try:
            if raw.startswith("in_"):
                download_invoice(raw)

            elif raw.startswith(("ch_", "py_")):
                ch = stripe.Charge.retrieve(raw, expand=["payment_intent"])
                # 1) старая схема
                inv_id = ch.get("invoice") or ch.get("payment_intent", {}).get("invoice")
                # 2) новая схема через InvoicePayment
                if not inv_id:
                    pi_id = ch.get("payment_intent", {}).get("id")
                    inv_id = invoice_from_payment(charge_id=raw) or (
                             invoice_from_payment(pi_id=pi_id) if pi_id else None)
                if inv_id: download_invoice(inv_id)
                else:      print(f"⚠️  {raw}: платёж без invoice")

            elif raw.startswith("pi_"):
                pi = stripe.PaymentIntent.retrieve(raw)
                inv_id = pi.get("invoice") or invoice_from_payment(pi_id=raw)
                if inv_id: download_invoice(inv_id)
                else:      print(f"⚠️  {raw}: PaymentIntent без invoice")

            else:
                print(f"🤷  Неизвестный ID: {raw}")

        except Exception as e:
            print(f"❌  {raw}: {e}")

        time.sleep(RATE_LIMIT_S)

if __name__ == "__main__":
    main()
