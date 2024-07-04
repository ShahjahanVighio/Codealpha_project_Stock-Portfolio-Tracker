import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Example API key (use your own from the chosen API service)
API_KEY = 'LXT0L6173VN1YVL0'
BASE_URL = 'https://www.alphavantage.co/query'


def get_stock_data(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '5min',
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if 'Time Series (5min)' in data:
        return data['Time Series (5min)']
    else:
        print(f"Error fetching data for symbol: {symbol}")
        return None


class Portfolio:
    def __init__(self):
        self.stocks = {}

    def add_stock(self, symbol, quantity):
        if symbol in self.stocks:
            self.stocks[symbol] += quantity
        else:
            self.stocks[symbol] = quantity

    def remove_stock(self, symbol, quantity):
        if symbol in self.stocks:
            if self.stocks[symbol] <= quantity:
                del self.stocks[symbol]
            else:
                self.stocks[symbol] -= quantity

    def get_portfolio_value(self):
        total_value = 0
        for symbol, quantity in self.stocks.items():
            stock_data = get_stock_data(symbol)
            if stock_data:
                latest_price = float(list(stock_data.values())[0]['4. close'])
                total_value += latest_price * quantity
        return total_value

    def display_portfolio(self):
        for symbol, quantity in self.stocks.items():
            print(f"{symbol}: {quantity} shares")


def main():
    portfolio = Portfolio()

    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Get Portfolio Value")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            symbol = input("Enter stock symbol: ")
            quantity = int(input("Enter quantity: "))
            portfolio.add_stock(symbol, quantity)
        elif choice == '2':
            symbol = input("Enter stock symbol: ")
            quantity = int(input("Enter quantity: "))
            portfolio.remove_stock(symbol, quantity)
        elif choice == '3':
            portfolio.display_portfolio()
        elif choice == '4':
            value = portfolio.get_portfolio_value()
            print(f"Total Portfolio Value: ${value:.2f}")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
