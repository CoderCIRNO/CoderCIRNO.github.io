# selenium

```python
from selenium import webdriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path="../chromeDriver/chromedriver", options=options)
driver.get("https://www.example.com/")

#oth 

status = driver.find_element_by_css_selector("#status-val > span")
if status.text == "开放":
    resolveButton = driver.find_element_by_css_selector("#action_id_71 > span")
    resolveButton.click()
    toInput = driver.find_element_by_css_selector("#comment")
    toInput.send_keys("M2不使用此文件")
```