
import csv
import yfinance as yf

STOCK_FILE = "constituents.csv"
OUTPUT_FILE = "portfolio_summary.csv"

portfolio = {}


# Load valid S&P 500 ticker symbols from CSV
def load_stocks():
    stocks = {}

    try:
        with open(STOCK_FILE, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                symbol = row["Symbol"].strip().upper()
                company = row["Security"].strip()

                stocks[symbol] = company

        return stocks

    except FileNotFoundError:
        print("Error: constituents.csv not found!")
        return {}


# Fetch latest available stock price
def get_stock_price(ticker):
    stock = yf.Ticker(ticker)

    # Try intraday data first
    data = stock.history(period="1d", interval="1m")

    # Fall back to recent daily data
    if data.empty:
        data = stock.history(period="5d", interval="1d")

    if data.empty:
        raise ValueError("Unable to retrieve stock price.")

    price = data["Close"].dropna().iloc[-1]

    return float(price)


# Main program
def main():

    stocks = load_stocks()

    if not stocks:
        print("Unable to load stock dataset.")
        return

    print("\n========== INVESTMENT PORTFOLIO TRACKER ==========")
    print("S&P 500 stock dataset loaded successfully.")

    while True:

        ticker = input(
            "\nEnter stock ticker (or DONE to finish): "
        ).strip().upper()

        if ticker == "DONE":
            break

        if ticker not in stocks:
            print("Invalid ticker! Please enter an S&P 500 ticker.")
            continue

        if ticker in portfolio:
            print("This stock is already in your portfolio.")
            continue

        try:
            buy_price = float(
                input("Enter purchase price per share: ")
            )

            quantity = int(
                input("Enter number of shares: ")
            )

            if buy_price <= 0 or quantity <= 0:
                print("Price and quantity must be positive.")
                continue

            print(f"\nFetching latest price for {ticker}...")

            current_price = get_stock_price(ticker)

            portfolio[ticker] = {
                "company": stocks[ticker],
                "buy_price": buy_price,
                "quantity": quantity,
                "current_price": current_price
            }

            print("Stock added successfully!")
            print("Company:", stocks[ticker])
            print(f"Latest available price: ${current_price:.2f}")

        except ValueError as error:
            print("Invalid input or price:", error)

        except Exception as error:
            print("Unable to retrieve stock data:", error)

    if not portfolio:
        print("\nNo stocks added to portfolio.")
        return

    total_investment = 0
    total_market_value = 0

    print("\n============== PORTFOLIO SUMMARY ==============")

    try:
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Ticker",
                "Company",
                "Buy Price",
                "Quantity",
                "Current Price",
                "Invested Amount",
                "Market Value",
                "Profit/Loss",
                "Gain/Loss Percentage"
            ])

            for ticker, details in portfolio.items():

                buy_price = details["buy_price"]
                quantity = details["quantity"]
                current_price = details["current_price"]

                invested = buy_price * quantity
                market_value = current_price * quantity

                profit_loss = market_value - invested

                percentage = (
                    profit_loss / invested
                ) * 100

                total_investment += invested
                total_market_value += market_value

                print(f"\nStock: {ticker}")
                print(f"Company: {details['company']}")
                print(f"Investment: ${invested:.2f}")
                print(f"Market Value: ${market_value:.2f}")
                print(f"Profit/Loss: ${profit_loss:.2f}")
                print(f"Gain/Loss: {percentage:.2f}%")

                writer.writerow([
                    ticker,
                    details["company"],
                    buy_price,
                    quantity,
                    current_price,
                    invested,
                    market_value,
                    profit_loss,
                    percentage
                ])

        total_profit_loss = (
            total_market_value - total_investment
        )

        total_percentage = (
            total_profit_loss / total_investment
        ) * 100

        print("\n========== TOTAL PORTFOLIO ==========")
        print(f"Total Investment: ${total_investment:.2f}")
        print(f"Total Market Value: ${total_market_value:.2f}")
        print(f"Total Profit/Loss: ${total_profit_loss:.2f}")
        print(f"Overall Gain/Loss: {total_percentage:.2f}%")

        print(f"\nReport saved successfully: {OUTPUT_FILE}")

    except OSError as error:
        print("Unable to save CSV report:", error)


if __name__ == "__main__":
    main()
