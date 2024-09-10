import requests                                  # 用於發送 HTTP 請求，向伺服器索取資料
import pandas as pd                              # 用於處理表格型數據，將爬取到的資料轉換成 DataFrame 格式
import calendar                                  # 提供與日曆相關的函數
import os                                        # 提供與操作系統相關的函數，用於建立檔案路徑
# get_twse_stock_data: 定義一個函數，用來獲取指定股票在指定日期範圍內的收盤價資料。
def get_twse_stock_data(stock_id, start_date, end_date):
    # url=選擇爬取資料的網站連結(TWSE 提供日收盤價資料)
    url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG" 
    params = {
        'response': 'json',                       # 指定回傳的資料格式為 JSON
        'date': f"{start_date}-{end_date}",       # 指定查詢的日期範圍{star_date}-{end_date}查尋起始日期到結束日期
        'stockNo': stock_id                       # stockNo=指定查尋股票代碼(stock_id)
    }
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()                              # 檢查response物件的狀態碼(顯示成功:200 , 顯示失敗:400)
        data = response.json()                                   # 將回傳的 json 格式資料轉換成 Python 的字典。
        df = pd.DataFrame(data['data'], columns=data['fields'])  # 將字典中的資料轉換成 Pandas 的 DataFrame 格式。
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")                       # 使用 f-string 格式化字符串，將錯誤訊息 (e) 打印到終端
        return None                                              # 如果發生錯誤，則不會返回任何資料，
                                                                 # 而是返回 None 值，告知調用此函式的程式碼資料獲取失敗。
# get_monthly_data: 呼叫 get_twse_stock_data 函數獲取資料，並將資料儲存為 CSV 檔案。                                                                 
def get_monthly_data(stock_id, year, month, save_dir):
    # 取得該月份的第一天和最後一天
    first_day = f"{year:04d}{month:02d}01"
    last_day = f"{year:04d}{month:02d}{calendar.monthrange(year, month)[1]}"
    # 呼叫 get_twse_stock_data 函數
    df = get_twse_stock_data(stock_id, first_day, last_day)
    # 建立儲存檔案的路徑
    file_name = f'{stock_id}_{first_day}_{last_day}_daily_avg.csv'
    save_path = os.path.join(save_dir, file_name)
    # 判斷 DataFrame df 是否有值。如果 df 存在且不為空（即包含資料），則執行下面的程式碼
    if df is not None:
        df.to_csv(save_path, index=False, encoding='utf-8-sig')   # 指定儲存檔案的編碼為 UTF-8 with signature
        print(f"Data saved to {save_path}")

# 設定股票代碼、日期範圍和儲存資料夾
stock_id = '00642U'                                # 股票代碼:(0050,0055,0056,00635U,00642U,00679B,00692,00711B,00712)
start_year = 2018                                 # 選取2018年開始
end_year = 2024                                   # 選取2024年結束
save_directory = "C:/projace0801/TWSE_CSV/00712"  # 替換為你想要的儲存資料夾路徑

# 逐月爬取資料並儲存
for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        get_monthly_data(stock_id, year, month, save_directory)