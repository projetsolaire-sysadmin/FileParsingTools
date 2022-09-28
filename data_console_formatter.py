import pandas as pd
import datetime as datetime
import numpy as np

def open():
    df = pd.read_csv('data/consumption.csv', sep=';', parse_dates=['date'])
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    df = df.dropna(how='all', axis='columns')
    df = df[df['value'].notna()]
    df = df.dropna()
    df = date_formatting(df)
    df = fill_forwards(df)
    print(df)
    df.to_csv("output/consumption.csv")


def date_formatting(df):
    year = df['date'].dt.year.add(-2).astype(str)
    month_day = df['date'].dt.strftime('%m%d')
    df["measurementDate"] = pd.to_datetime(year + month_day, format='%Y%m%d')
    df['measurementHour'] = df['date'].dt.strftime('%H:%M')
    df = df.drop('date', axis=1)
    df = df.set_index('measurementDate')
    return df

def fill_forwards(df):
    dateOfLastRow = df.index[-1]
    yearOfLastRow = dateOfLastRow.year
    print(yearOfLastRow)
    previousYear = yearOfLastRow - 1
    endOfPreviousYear = datetime.datetime(previousYear, 12, 31)
    dateOfLastRowInPreviousYear = datetime.datetime(previousYear, dateOfLastRow.month, dateOfLastRow.day)
    print(yearOfLastRow)
    rng = df[(df.index > dateOfLastRowInPreviousYear) & (df.index <= endOfPreviousYear)]
    rng.index = rng.index + np.timedelta64(365,'D')
    merge = pd.concat([df, rng])
    merge.index = merge.index.strftime('%d-%m-%Y')
    #df2 = merge.loc['2020']
    #df2.index = df2.index + np.timedelta64(365,'D')
    #merge = pd.concat([merge, df2])
    return merge

def fill_backwards():
    pass


def run():
    open()


if __name__ == '__main__':
    run()