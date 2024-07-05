from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


def game_finder(link1,link2):
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    browser.get('https://ru.dltv.org/matches')
    matches = browser.find_elements(By.CLASS_NAME, "live__matches-item")
    useragent = UserAgent()
    ua = useragent.random
    print(ua)
    options.add_argument(f"user-agent ={ua}")
    for match in matches:
        livematches = match.find_elements(By.CLASS_NAME, "live__matches-item__body")
        if livematches:
            for el in livematches:
                url = el.find_element(By.TAG_NAME, 'a').get_attribute('href')
                print(url)


game_finder()
