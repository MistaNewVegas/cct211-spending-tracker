import numpy as np
import pandas as pd


def read_csv_as_df(file_location: str):
    """ open a csv, return as dataframe """
    with open(file_location, 'r') as file:
        df = pd.read_csv(file)
        return df       

def total_spending_over_time(df, start: str, end: str) -> float: # ex: 03152024-03162024
    """ Returns total expenditure over specified time range """
    df['date'] = pd.to_datetime(df['date']) # converts row to datetime format (temp)
    df.set_index('date', inplace=True) # sets date as index
    filtered_df = df[start:end] # filtered by date
    total = round(filtered_df['amount'].sum(), 2)
    return f'total expenditure from {start} to {end}: {total}'

def budget_balance(daily_budget=None, weekly_budget=None, monthly_budget=None) -> float:
    """ returns spending money left """
# looking back a lot of this stuff is pointless - will clean up with time.

df = read_csv_as_df('sheet.csv')
result = total_spending_over_time(df, '2022-05-15', '2024-03-17')

print(result)
