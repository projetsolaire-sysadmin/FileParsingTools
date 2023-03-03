import pandas as pd

import ntpath



PRODUCTION_RENAMING_HEADER_MAP = {'Month': 'month', 'Day': 'day', 'Hour': 'hour', 'Energy Production [kWh]': 'value'}
CONSUMPTION_PARSED_DATE_FORMAT = ""

def parse_production2(file):
    df = pd.read_csv(file, index_col=0)
    df = rename_columns(df)
    df = df.set_index('month')
    # print(df)
    output_file_name = 'app/output_formated/'+ntpath.basename(file)[:-4]+'_output.csv'
    print(output_file_name)
    df.to_csv(output_file_name)
    return output_file_name


def rename_columns(df):
    df.rename(columns=PRODUCTION_RENAMING_HEADER_MAP, inplace=True)
    return df

# def rebase_to_2020(df):
#     year = df['measurementDate'].dt.year.add(-1).astype(str)
#     month_day = df['measurementDate'].dt.strftime('%m%d')
#     df["measurementDate"] = pd.to_datetime(year + month_day, format='%Y%m%d')
#     df['measurementDate'] = df['measurementDate'].dt.strftime('%d-%m-%Y')
#     df = df.set_index('measurementDate')
#     return df

if __name__ == '__main__':
    parse_production2('upload_files/Aurora-Solar-Format.csv')

