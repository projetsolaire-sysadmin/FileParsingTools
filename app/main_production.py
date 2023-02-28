import pandas as pd

PRODUCTION_RENAMING_HEADER_MAP = {'Month': 'month', 'Day': 'day', 'Hour': 'hour', 'Energy Production [kWh]': 'value'}
CONSUMPTION_PARSED_DATE_FORMAT = ""

def parse_production():
    df = pd.read_csv('data/production.csv', index_col=0)
    df = rename_columns(df)
    df = df.set_index('month')
    print(df)
    df.to_csv('output/production.csv')


def rename_columns(df):
    df.rename(columns=PRODUCTION_RENAMING_HEADER_MAP, inplace=True)
    return df

# def parse_consumption():
#     df = pd.read_csv('data/consumption.csv')
#     df['measurementDate'] = pd.to_datetime(df.measurementDate, format='%d/%m/%Y')
#     df = rebase_to_2020(df)
#     print(df)
#     df.to_csv('output/consumption.csv')

def change_date_format():
    pass

def rebase_to_2020(df):
    year = df['measurementDate'].dt.year.add(-1).astype(str)
    month_day = df['measurementDate'].dt.strftime('%m%d')
    df["measurementDate"] = pd.to_datetime(year + month_day, format='%Y%m%d')
    df['measurementDate'] = df['measurementDate'].dt.strftime('%d-%m-%Y')
    df = df.set_index('measurementDate')
    return df


if __name__ == '__main__':
    parse_production()

