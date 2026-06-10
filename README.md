# 📈 AI Stock Screener Indonesia

AI-powered stock screener untuk saham Indonesia (IDX) menggunakan:

* Streamlit Dashboard
* Technical Analysis Engine
* AI Scoring System
* Telegram Notification
* Paper Trading
* Backtesting Engine
* Supabase Database
* GitHub Actions Automation

---

# 🚀 Features

## ✅ AI Stock Screener

Screening otomatis saham IDX berdasarkan:

* Trend structure
* RSI momentum
* Volume breakout
* Bollinger breakout
* MACD momentum
* ADX trend strength
* ATR volatility filter

---

## ✅ Market Regime Detection

Deteksi kondisi market:

* Bullish
* Bearish
* Sideways

berdasarkan IHSG.

---

## ✅ Morning Confirmation

Validasi intraday:

* Gap analysis
* Candle structure
* Volume confirmation

---

## ✅ Telegram Notification

Auto send signal ke Telegram:

* Night screener
* Morning confirmation
* Trade audit
* TP / SL notification

---

## ✅ Paper Trading

Simulasi trading:

* Buy
* Stop loss
* Take profit
* Auto close

---

## ✅ Backtesting

Backtest strategy menggunakan:

* MA crossover
* RSI momentum
* Volume breakout

---

## ✅ Automation

GitHub Actions automation:

* Night screener
* Morning confirmation
* Trade audit

---

# 📂 Project Structure

```bash
AI-Stock-Screener/
│
├── .github/
│   └── workflows/
│
├── core/
│
├── database/
│
├── runners/
│
├── dashboard/
│
├── watchlist/
│
├── tests/
│
├── logs/
│
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/your-username/AI-Stock-Screener.git
```

---

## 2. Open Project

```bash
cd AI-Stock-Screener
```

---

## 3. Create Virtual Environment

```bash
python -m venv venv
```

---

## 4. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create `.env`

```env
SUPABASE_URL=your_url
SUPABASE_KEY=your_key

TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

# ▶️ Run Dashboard

```bash
streamlit run dashboard/app.py
```

---

# 🤖 Run AI Screener

```bash
python runners/auto_screener.py
```

---

# ☀️ Run Morning Confirmation

```bash
python runners/morning_confirmation_runner.py
```

---

# 📊 Run Trade Audit

```bash
python runners/trade_audit_runner.py
```

---

# 🧠 AI Scoring Logic

Scoring menggunakan:

* MA Trend
* EMA Trend
* RSI
* MACD
* ADX
* Volume Analysis
* Breakout Detection
* ATR Volatility
* Bollinger Expansion

---

# 📡 Deployment

Recommended:

* GitHub Actions
* Streamlit Cloud
* Supabase

---

# ⚠️ Disclaimer

This project is for educational purposes only.

Not financial advice.

Trade at your own risk.

---

# 👨‍💻 Author

Danang Susilo

Indonesia AI Trading Project
