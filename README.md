# 📈 AI Stock Screener Indonesia

AI-powered swing trading platform untuk saham Indonesia (IDX) menggunakan:

- Streamlit Dashboard
- AI Technical Scoring
- Market Regime Detection
- Relative Strength Analysis
- Telegram Automation
- Paper Trading
- Backtesting Engine
- AI Learning Engine
- Supabase Database
- GitHub Actions Automation

---

# 🚀 Features

## ✅ AI Stock Screener

Screening otomatis saham IDX berdasarkan:

- Trend Structure
- EMA & MA Alignment
- RSI Momentum
- MACD Momentum
- ADX Trend Strength
- Relative Volume
- Bollinger Expansion
- ATR Volatility Filter
- Breakout Detection
- Relative Strength vs IHSG

---

## ✅ Market Regime Detection

Deteksi kondisi market otomatis berdasarkan IHSG:

- STRONG_BULL
- BULL
- ACCUMULATION
- SIDEWAYS
- DISTRIBUTION
- BEARISH
- PANIC
- RECOVERY

---

## ✅ Market Breadth Analysis

Analisis kesehatan market:

- % saham di atas MA20
- RSI Breadth
- Breakout Breadth
- Relative Strength Breadth

---

## ✅ Sector Strength Analysis

Ranking sektor IDX berdasarkan:

- Average Return
- Relative Strength
- RSI Momentum
- Bullish Breadth

---

## ✅ Morning Confirmation Engine

Validasi intraday setup menggunakan:

- Gap Analysis
- Candle Structure
- Volume Confirmation
- Intraday Momentum
- Trend Confirmation

---

## ✅ Telegram Automation

Auto notification ke Telegram:

- Night Screener
- Morning Confirmation
- Trade Audit
- Stop Loss Hit
- Take Profit Hit
- Market Commentary

---

## ✅ Paper Trading

Simulasi trading otomatis:

- Buy
- Stop Loss
- Take Profit
- Auto Close
- PnL Tracking
- Portfolio Analytics

---

## ✅ Backtesting Engine

Backtest strategy menggunakan:

- MA Structure
- RSI Momentum
- Volume Breakout
- Risk Management

---

## ✅ AI Learning Engine

AI mengevaluasi performa strategy berdasarkan:

- Market Regime
- Confidence Score
- Winrate
- Profitability

---

## ✅ Dashboard Analytics

Interactive dashboard menggunakan Streamlit:

- Market Snapshot
- Screener Dashboard
- Portfolio Dashboard
- Analytics Dashboard
- AI Learning Dashboard
- Forward Testing Dashboard
- System Health Dashboard

---

# 📂 Project Structure

```bash
AI-Stock-Screener/
│
├── app/
│   ├── dashboard/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── utils/
│   │   └── app.py
│   │
│   └── runners/
│
├── ai/
├── analytics/
├── market/
├── portfolio/
├── screener/
├── storage/
├── strategies/
├── trading/
├── database/
├── watchlist/
├── tests/
├── logs/
├── data/
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

# 📦 Requirements

- Python 3.11+
- Streamlit
- Pandas
- NumPy
- Plotly
- YFinance
- Supabase
- TA
- Backtesting.py

---

# 🔐 Environment Variables

Create `.env`

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

# ⬇️ Download Market Data

Sebelum menjalankan screener:

```bash
python app/runners/download_market_data.py
```

---

# ▶️ Run Dashboard

```bash
streamlit run app/dashboard/app.py
```

---

# 🤖 Run AI Screener

```bash
python app/runners/auto_screener.py
```

---

# ☀️ Run Morning Confirmation

```bash
python app/runners/morning_confirmation_runner.py
```

---

# 📊 Run Trade Audit

```bash
python app/runners/trade_audit_runner.py
```

---

# 🧪 Run Backtest

Example:

```python
from backtest import run_backtest

stats = run_backtest("BBRI.JK")

print(stats)
```

---

# 🧠 AI Scoring Logic

Scoring menggunakan kombinasi:

- MA Trend Structure
- EMA Structure
- RSI Momentum
- MACD Momentum
- ADX Trend Strength
- Volume Expansion
- Breakout Confirmation
- ATR Volatility
- Bollinger Expansion
- Relative Strength

---

# 📡 Automation

GitHub Actions automation:

- Night Screener
- Morning Confirmation
- Trade Audit
- Backup System

---

# ☁️ Deployment

Recommended stack:

- Streamlit Cloud
- GitHub Actions
- Supabase

---

# ⚠️ Disclaimer

This project is for educational purposes only.

Not financial advice.

Trade at your own risk.

---

# 👨‍💻 Author

Danang Susilo

Indonesia AI Trading Project
