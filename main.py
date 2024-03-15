import pandas as pd

def clean_and_format(file_location:str):
    df = pd.read_csv(file_location)
    df['date'] = pd.to_datetime(df['date'])
    df.to_csv(file_location, index=False)
    print(df.head)

def prompted_csv_append(file_location:str):
    df = pd.read_csv(file_location, index_col=False)
    columns = df.columns.tolist()
    receipt = {'name': None, 'amount': None, 'date': None, 'description': None}
    for column in columns:
        match column:
            case 'name': 
                receipt['name'] = input("Please enter a short name of the purchase: ")
            case 'amount': 
                receipt['amount'] = float(input("Please enter the amount spent X.XX: "))
            case 'date': 
                receipt['date'] = input("please enter the date in YYYY-MM-DD format: ")
            case 'description': 
                receipt['description'] = input("write a brief description about the purchase: ")

    receipt_df = pd.DataFrame([receipt])
    df = pd.concat([df, receipt_df], ignore_index=True)
    df.to_csv(file_location, index=False)

 

clean_and_format('sheet.csv')
# prompted_csv_append('sheet.csv')