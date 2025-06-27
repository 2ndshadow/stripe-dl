# Stripe Invoice Downloader

The script `download_invoices.py` automatically saves PDF invoices by a list of **Invoice / Charge / PaymentIntent** IDs. Works on macOS, Linux, and Windows.

---

## 1. What the script does

* Reads the file `invoice_ids.csv` (one ID per line). Supported:
  * `in_…` — Invoice ID
  * `ch_…`, `py_…` — Charge ID
  * `pi_…` — PaymentIntent ID
* For each ID, determines where the invoice is and downloads the `invoice_pdf`.
* Saves files to the **`invoices/`** folder as `in_XXXXXXXX.pdf`.

---

## 2. Requirements

* **Python 3.8+**
* Packages: `stripe`, `requests`, `python-dotenv`
* Stripe API key with **Invoices → Read, Charges → Read, Payment Intents → Read** permissions.

---

## 3. Installation

```bash
# 1. Clone the repository or place the script in a separate folder
cd ~/projects/stripe-dl

# 2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install stripe requests python-dotenv
```

---

## 4. Setup

1. **API key**  
   In the project root, create a `.env` file:

   ```env
   STRIPE_SECRET_KEY=rk_live_xxxxxxxxxxxxxxxxxxxx
   ```

   Restrict the key's permissions (Invoices/Charges/PaymentIntents → Read).

2. **ID list**  
   The file `invoice_ids.csv`, format:

   ```
   ch_3RJtDGBkBGkwtT0Q1VZTeGkO
   in_1P9abcDefGhijKLmn
   pi_3RK4…
   ```

---

## 5. Usage

```bash
source .venv/bin/activate      # if the environment is not yet active
python download_invoices.py    # PDFs will appear in ./invoices/
```

Progress is printed to the console: ✔ — saved, ⚠️ — invoice not found, ❌ — error.

---


## 6. Stripe API version update

The script is compatible with versions **up to** 2025-03-31 and newer.  
To support future changes, update the `stripe` package:

```bash
pip install --upgrade stripe
```


