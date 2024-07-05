from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from collections import defaultdict
import telebot
from fake_useragent import UserAgent


def live():
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    browser.get('https://ru.dltv.org/matches')
    matches = browser.find_elements(By.CLASS_NAME, "matches")
    useragent = UserAgent()
    ua = useragent.random
    print(ua)
    options.add_argument(f"user-agent ={ua}")
    all_games = []
    id = []
    dates = browser.find_elements(By.CLASS_NAME, "live__matches-item")
    for date in dates:
        id1 = date.get_attribute("data-series-id")
        id.append(id1)
    for match in matches:
        livematches = match.find_elements(By.CLASS_NAME, "live__matches-item__body")
        if livematches:
            for el in livematches:
                teams = el.find_elements(By.CLASS_NAME, "match__item-team__name")
                if len(teams) == 2:
                    games = []
                    team1 = teams[0].text.replace("\nСилы света", "").replace("\nСилы тьмы", "")
                    team2 = teams[1].text.replace("\nСилы света", "").replace("\nСилы тьмы", "")
                    games.extend([team1, team2])
                    all_games.append(games)
        else:
            return "Лайв матчей нет"
    browser.close()
    browser.quit()
    return all_games , id


def upcoming():
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    browser.get('https://ru.dltv.org/matches')
    matches = browser.find_elements(By.CLASS_NAME, "matches")
    # useragent = UserAgent()
    # ua = useragent.random
    # print(ua)
    # options.add_argument(f"user-agent ={ua}")
    all_data = []
    all_games = []
    id = []
    dates = browser.find_elements(By.CLASS_NAME, "upcoming__matches-item")
    for date in dates:
        data = date.get_attribute("data-matches-odd")[:10]
        all_data.append(data)
        id1 = date.get_attribute("data-series-id")
        id.append(id1)
    for match in matches:
        upmatches = match.find_elements(By.CLASS_NAME, "upcoming__matches-item__body")
        if upmatches:
            for el in upmatches:
                teams = el.find_elements(By.CLASS_NAME, "match__item-team__name")
                if len(teams) == 2:
                    games = []
                    team1 = teams[0].text.replace("\nСилы света", "").replace("\nСилы тьмы", "")
                    team2 = teams[1].text.replace("\nСилы света", "").replace("\nСилы тьмы", "")
                    games.extend([team1, team2])
                    all_games.append(games)
    matches_dict = defaultdict(list)
    for date, team in zip(all_data, all_games):
        matches_dict[date].append(team)
    matches_dict = dict(matches_dict)
    return matches_dict


def results():
    options = Options()
    options.add_argument("--headless")
    useragent = UserAgent()
    ua = useragent.random
    print(ua)
    browser = webdriver.Chrome(options=options)
    browser.get('https://ru.dltv.org/results')
    matches = browser.find_elements(By.CLASS_NAME, "matches")
    all_data = []
    all_games = []
    id = []
    dates = browser.find_elements(By.CLASS_NAME, "result__matches-item")
    for date in dates:
        data = date.get_attribute("data-matches-odd")[:10]
        all_data.append(data)
        id1 = date.get_attribute("data-series-id")
        id.append(id1)
    for match in matches:
        resmatches = match.find_elements(By.CLASS_NAME, "result__matches-item__body")
        if resmatches:
            for el in resmatches:
                teams = el.find_elements(By.CLASS_NAME, "match__item-team__name")
                if len(teams) == 2:
                    games = []
                    team1 = teams[0].text.replace("\nСилы света", "").replace("\nСилы тьмы", "")
                    team2 = teams[1].text.replace("\nСилы света", "").replace("\nСилы тьмы", "")
                    games.extend([team1, team2])
                    all_games.append(games)
    matches_dict = defaultdict(list)
    for date, team in zip(all_data, all_games):
        matches_dict[date].append(team)
    matches_dict = dict(matches_dict)
    return matches_dict, id


def userans(func):
    games = func
    game_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for game in games:
        button = telebot.types.KeyboardButton(" vs ".join(game))
        game_keyboard.add(button)
    return game_keyboard
