import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import easyocr
import time


# 브라우저 크롤링 감지 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1920, 1080)
interpark_url = 'https://tickets.interpark.com/'

driver.implicitly_wait(time_to_wait=2)
driver.get(url=interpark_url)

# 로그인
driver.find_element(By.LINK_TEXT, '로그인').click()
userId = driver.find_element(By.ID, 'userId')
userId.send_keys('')
userPwd = driver.find_element(By.ID, "userPwd")
userPwd.send_keys('')
userPwd.send_keys(Keys.ENTER)

# 티켓 사이트 이동
driver.get("https://tickets.interpark.com/goods/24013437")
driver.find_element(By.CSS_SELECTOR, ".popupCloseBtn.is-bottomBtn").click()
driver.find_element(By.CSS_SELECTOR, ".sideBtn.is-primary").click()

# 팝업진입/부정예매방지 문자 입력
time.sleep(5) # 로딩 대기
driver.switch_to.window(driver.window_handles[-1])
driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmSeat']"))
reader = easyocr.Reader(['en'])
captcha_png = driver.find_element(By.ID, "imgCaptcha")

while captcha_png:
    result = reader.readtext(captcha_png.screenshot_as_png, detail=0)
    capcha_value = result[0].replace(' ', '').replace('5', 'S').replace('0', 'O').replace('$', 'S').replace(',', '') \
        .replace(':', '').replace('.', '').replace('+', 'T').replace("'", '').replace('`', '') \
        .replace('1', 'L').replace('e', 'Q').replace('3', 'S').replace('€', 'C').replace('{', '').replace('-', '')

    # 입력
    driver.find_element(By.XPATH, '//*[@id="divRecaptcha"]/div[1]/div[3]').click()
    captcha_txt = driver.find_element(By.XPATH, '//*[@id="txtCaptcha"]')
    captcha_txt.send_keys(capcha_value)

    # 입력완료 버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="divRecaptcha"]/div[1]/div[4]/a[2]').click()

    display = driver.find_element(By.XPATH, '//*[@id="divRecaptcha"]').is_displayed()
    if display:
        # 새로고침
        driver.find_element(By.XPATH, '//*[@id="divRecaptcha"]/div[1]/div[1]/a[1]').click()
    else:
        break
