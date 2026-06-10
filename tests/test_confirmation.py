import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from core.confirmation import (
    morning_confirmation
)

# ======================================
# TEST SINGLE STOCK
# ======================================

def test_single_confirmation():

    print(
        "☀️ Testing single confirmation..."
    )

    symbol = "BBCA.JK"

    result = morning_confirmation(
        symbol
    )

    print(
        f"📊 {symbol}: {result}"
    )


# ======================================
# TEST MULTIPLE STOCKS
# ======================================

def test_multiple_confirmations():

    print(
        "📈 Testing multiple confirmations..."
    )

    symbols = [

        "BBCA.JK",

        "TLKM.JK",

        "BMRI.JK",

        "ASII.JK",

        "BBRI.JK"
    ]

    results = []

    for symbol in symbols:

        try:

            confirmation = (
                morning_confirmation(
                    symbol
                )
            )

            results.append({

                "symbol": symbol,

                "confirmation": confirmation
            })

            print(
                f"✅ {symbol}: "
                f"{confirmation}"
            )

        except Exception as e:

            print(
                f"❌ Error {symbol}: {e}"
            )

    # ======================================
    # SUMMARY
    # ======================================

    print("\n📋 SUMMARY")

    for result in results:

        print(

            f"{result['symbol']} → "

            f"{result['confirmation']}"
        )


# ======================================
# TEST SIGNAL QUALITY
# ======================================

def test_signal_quality():

    print(
        "🧠 Testing signal quality..."
    )

    symbols = [

        "BBCA.JK",

        "AMMN.JK",

        "BRPT.JK"
    ]

    for symbol in symbols:

        signal = morning_confirmation(
            symbol
        )

        print(
            f"{symbol}: {signal}"
        )

        if signal == "STRONG BUY":

            print(
                "🚀 Institutional breakout detected"
            )

        elif signal == "BUY":

            print(
                "✅ Valid momentum setup"
            )

        elif signal == "WATCH":

            print(
                "👀 Need more confirmation"
            )

        elif signal == "WEAK":

            print(
                "⚠️ Weak momentum"
            )

        elif signal == "AVOID":

            print(
                "❌ High risk setup"
            )

        else:

            print(
                "⚠️ Unknown signal"
            )

        print("-" * 40)


# ======================================
# MAIN TEST RUNNER
# ======================================

if __name__ == "__main__":

    print(
        "🚀 Running Confirmation Tests..."
    )

    print("=" * 50)

    test_single_confirmation()

    print("=" * 50)

    test_multiple_confirmations()

    print("=" * 50)

    test_signal_quality()

    print("=" * 50)

    print(
        "✅ Confirmation tests completed"
    )