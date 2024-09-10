import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_twse_stock_data(stock_id, year):
    """
    爬取指定股票在指定年份的日收盤價及月平均價

    Args:
        stock_id (str): 0050
        year (int): 2023

    Returns:
        pandas.DataFrame: 0050
    """

    url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG"
    params = {
        'response': 'json',
        'date': f'{year}0101-{year}1231',
        'stockNo': stock_id
    }

    # 發送請求並解析 JSON
    response = requests.post(url, params=params)
    data = response.json()

    # 將資料轉換成 Pandas DataFrame
    df = pd.DataFrame(data['data'], columns=data['fields'])
    return df

# 範例用法
stock_id = '0050'  # 台積電
year = 2022

df = get_twse_stock_data(stock_id, year)
print(df)

# 將資料儲存為 CSV
df.to_csv(f'{stock_id}_{year}_daily_avg.csv', index=False)