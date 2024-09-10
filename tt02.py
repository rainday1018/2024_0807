import twstock
import pandas as pd
import twstock.stock
# 導入twstock及pandas模組，pandas模組縮寫為pd

target_stock = '00679B'  #股票代號變數
stock = twstock.Stock(target_stock)  #告訴twstock我們要查詢的股票
target_price = stock.fetch_from(2024, 7)  #取用2020/05至今每天的交易資料
print(target_price)
target_close = [{'收盤價': target.close} for target in target_price]
target_data = [{'日期': target.date} for target in target_price]
target_all =[target_close, target_data]
df = pd.DataFrame(data=target_all)
#將twstock抓到的清單轉成Data Frame格式的資料表

filename = f'./TWSE_CSV/{target_stock}_ex.csv'
#指定Data Frame轉存csv檔案的檔名與路徑

df.to_csv(filename)
#將Data Frame轉存為csv檔案

