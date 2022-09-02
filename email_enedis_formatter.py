import pandas as pd

def open():
    df = pd.read_csv('data/consumption.csv', sep=';')
    df = df.set_index('Date')
    df = df.dropna(how='all', axis='columns')
    df = df[df['Value'].notna()]
    print(df)
    df = df.dropna()
def run():
    open()


if __name__ == '__main__':
    run()