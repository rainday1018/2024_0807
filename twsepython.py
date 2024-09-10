import requests
import pandas as pd

def get_twse_stock_data(stock_id, start_date, end_date):
    """
    爬取指定股票在指定期間的日收盤價及月平均價

    Args:
        stock_id (str): 股票代碼
        start_date (str): 起始日期 (YYYYMMDD)
        end_date (str): 結束日期 (YYYYMMDD)

    Returns:
        pandas.DataFrame: 爬取到的資料
    """

    url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG"
    params = {
        'response': 'json',
        'date': f"{start_date}-{end_date}",
        'stockNo': stock_id
    }

    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['data'], columns=data['fields'])
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# 設定股票代碼和日期範圍
stock_id = '0050'
start_date = '20170101'
end_date = '20240731'

# 爬取資料
df = get_twse_stock_data(stock_id, start_date, end_date)

# 儲存為 CSV 檔案
if df is not None:
    df.to_csv(f'{stock_id}_{start_date}_{end_date}_daily_avg.csv', index=False, encoding='utf-8-sig')
    print(f"Data saved to {stock_id}_{start_date}_{end_date}_daily_avg.csv")
else:
    print("Failed to fetch data.")