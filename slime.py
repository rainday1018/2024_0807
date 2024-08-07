from selenium import webdriver     # 匯入(import) 操控瀏覽器相關的程式
from selenium.webdriver.common.keys import Keys    # 操作瀏覽器互動的程式
from selenium.webdriver.common.by import By #Done tree
import time
driver = webdriver.Firefox()  #生成一個由程式操控的firefox
time.sleep(5)
driver.get("http://www.python.org") #訪問python.org
assert "Python" in driver.title    #檢查分業名稱是否含python
time.sleep(5)
elem = driver.find_element(By.NAME, "q")  #等同於BeautifulSoup的find
elem.clear()                              #清除搜尋欄
elem.send_keys("pycon")                   #輸入pycon到搜尋欄
elem.send_keys(Keys.RETURN)               #按下按鍵的enter
assert "No results found." not in driver.page_source # No reusults found 未出現在頁面上
driver.close()                             #關閉當前頁面
driver.quit()                              #關掉整個模擬瀏覽器
print("Done")