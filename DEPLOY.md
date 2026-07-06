# Replit Deployment Guide

## 1. Replit'ga import qilish

**Variant A: GitHub'dan to'g'ridan-to'g'ri import**
1. Replit → "+ Create Repl" → "Import from GitHub"
2. URL: `https://github.com/KRYZENSYS/kryzen-telegram-business`
3. Language: Python

**Variant B: Git clone qilib yuklash**
```bash
# Replit shell'da:
git clone https://github.com/KRYZENSYS/kryzen-telegram-business.git
cd kryzen-telegram-business
pip install -r requirements.txt
```

## 2. Secrets sozlash

🔒 **Secrets** bo'limiga quyidagilarni qo'ying (UI orqali, .env ga EMAS):

| Secret | Qayerdan olish | Majburiy |
|---|---|---|
| `BOT_TOKEN` | @BotFather → /newbot | Ha |
| `SUPER_ADMIN_ID` | @userinfobot | Ha |
| `JWT_SECRET` | `python3 -c "import secrets;print(secrets.token_urlsafe(48))"` | Ha |
| `ENCRYPTION_KEY` | `python3 -c "from cryptography.fernet import Fernet;print(Fernet.generate_key().decode())"` | Ha |
| `GROQ_API_KEY` | https://console.groq.com (bepul) | Ixtiyoriy |

Yoki `bash scripts/replit_setup.sh` ishga tushiring va chiqqan qiymatlarni Secrets'ga qo'ying.

## 3. Run

`.replit` fayli `python main.py` ni ishga tushiradi. "Run" tugmasini bosing.

Web panel: chap tarafdagi Webview → KRYZEN dashboard.

Bot: Telegram'da botingizga /start yuboring.

## 4. 24/7 ishlashi uchun

- **Replit Pro/Teams** → "Always On" yoqilsin.
- **Bepul reja** → har 5-10 daqiqada webview'ga kirib turish kerak (yoki Replit "Deployments" → "Autoscale" ga o'tkazish).
- **Yoki** UptimeRobot.com orqali `https://your-repl.repl.co/health` ga har 5 daqiqada ping yuboring.

## 5. Production ko'chirish

Hohlasangiz VPS'ga ko'chirishingiz mumkin — `requirements.txt` to'liq, faqat `.replit` va `replit.nix` ni e'tiborsiz qoldiring.
