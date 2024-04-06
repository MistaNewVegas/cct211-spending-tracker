import json
from datetime import datetime, timedelta
import pandas as pd
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import csv, os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class BudgetManager:
    def __init__(self):
        self.config_path = 'config.json'
        self.csv_file_path = 'sheet.csv'
        self.budgets = self.read_budget_config()
        self.transactions_df = self.read_csv_as_df()
        
        self.date_now = datetime.now()
        self.current_day = self.date_now.day
        self.current_month = self.date_now.month
        self.current_year = self.date_now.year

        self.last_week = self.date_now - timedelta(days=7)
        self.last_month = self.date_now - relativedelta(months=1)
        self.last_year = self.date_now - relativedelta(years=1)

        self.daily_budget_balance = self.calculate_todays_balance()
        self.weekly_budget_balance = self.calculate_period_balance(self.last_week, self.date_now, 'weekly_budget')
        self.monthly_budget_balance = self.calculate_period_balance(self.last_month, self.date_now, 'monthly_budget')
        self.annual_budget_balance = self.calculate_period_balance(self.last_year, self.date_now, 'annual_budget')

    def read_budget_config(self):
        """Read budget settings from config.json."""
        with open(self.config_path, 'r') as file:
            config = json.load(file)
            self.daily_budget = float(config['user']['daily_budget'])
            self.weekly_budget = float(config['user']['weekly_budget'])
            self.monthly_budget = float(config['user']['monthly_budget'])
            self.annual_budget = self.monthly_budget*12

    def read_csv_as_df(self):
        """Open a CSV file and return as DataFrame."""
        df = pd.read_csv(self.csv_file_path)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = df['amount'].replace({r'\$': '', ',': '', ' ': ''}, regex=True).astype(float)
        return df


    def calculate_todays_balance(self):
        """Calculate the budget balance for today."""
        transactions = self.transactions_df[self.transactions_df['date'].dt.date == self.date_now]
        total_spent = transactions['amount'].sum()
        return round((self.daily_budget - total_spent),2)

    def calculate_period_balance(self, start_date, end_date, budget_key):
        """Calculate the budget balance for a given period."""
        mask = (self.transactions_df['date'] >= start_date) & (self.transactions_df['date'] <= end_date)
        filtered_df = self.transactions_df.loc[mask]
        
        total_spent = filtered_df['amount'].sum()
        match budget_key:
            case 'weekly_budget': budget_amount = self.weekly_budget
            case 'monthly_budget': budget_amount = self.monthly_budget
            case 'annual_budget': budget_amount = self.annual_budget
        return round((budget_amount - total_spent),2)

class Graphs():
    def __init__(self):
        super().__init__()

        self.csv = "sheet.csv"

        self.date_now = datetime.now()
        self.current_day = self.date_now.day
        self.current_month = self.date_now.month
        self.current_year = self.date_now.year

        self.last_week = self.date_now - timedelta(days=7)
        self.last_month = self.date_now - relativedelta(months=1)
        self.last_year = self.date_now - relativedelta(years=1)

        self.update_graphs(self.csv)

    def update_graphs(self, csv):

        self.check_if_can_generate(csv)

        if self.can_generate_graphs:
            with open(csv, 'r') as file:
                df = pd.read_csv(file)
                df['date'] = pd.to_datetime(df['date'])

            self.weekly_line = self.line_by_day(df, self.last_week, self.date_now, "weekly")
            self.monthly_line = self.line_by_day(df, self.last_month, self.date_now, "monthly")
            self.annual_line = self.line_by_week(df, self.last_year, self.date_now, "annual")

            
    def check_if_can_generate(self, csv) -> list[str]:
        with open(csv, 'r') as file:
            df = pd.read_csv(file)

        if len(df) <= 10: 
            self.can_generate_graphs = False
        else: 
            self.can_generate_graphs = True
        
    
    def line_by_day(self, df, start, stop, period):

        # filter df
        mask = (df['date'] >= start) & (df['date'] <= stop)
        filtered_df = df.loc[mask]

        # Aggregate expenses by day
        daily_sums = filtered_df.groupby('date')['amount'].sum()

        # Plot
        plt.figure(figsize=(10, 6))
        plt.plot(daily_sums.index, daily_sums.values, marker='o', linestyle='-')
        
        # Formatting
        plt.xlabel("Date")
        plt.ylabel("Sum of Expenses ($)")
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        plt.grid(True)

        temp_dir = 'graphs'
        file_name = f"line_{period}.png"
        file_path = os.path.join(temp_dir, file_name)
        plt.savefig(file_path)
        plt.close()

        return file_path
    
    def line_by_week(self, df, start, stop, period):

        # filter df
        mask = (df['date'] >= start) & (df['date'] <= stop)
        filtered_df = df.loc[mask]

        # Aggregate expenses by week
        daily_sums = filtered_df.groupby(pd.Grouper(key='date', freq='W'))['amount'].sum()

        # Plot
        plt.figure(figsize=(10, 6))
        ax = plt.subplot(111)
        ax.plot(daily_sums.index, daily_sums.values, marker='o', linestyle='-', linewidth=2, markersize=8)

        # Default formatting (remove fancy styling and colors)
        plt.xlabel("Date", fontsize=14)
        plt.ylabel("Sum of Expenses ($)", fontsize=14)
        plt.xticks(rotation=45, fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()

        # Save plot
        temp_dir = 'graphs'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        file_name = f"line_{period}.png"
        file_path = os.path.join(temp_dir, file_name)
        plt.savefig(file_path)
        plt.close()

        # Return path for further use
        return file_path
    
