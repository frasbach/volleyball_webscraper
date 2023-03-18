from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from sqlalchemy import CursorResult
from cup import Cup
import database as db
import time
import datetime
from bot import MessageBot


def createDriver():
  chromeOptions = webdriver.ChromeOptions()
  chromeOptions.add_argument("headless")
  return webdriver.Chrome(options=chromeOptions)


def setupDB():
  db.setUp()

def find_gender(gender_string: str):
  if gender_string == 'm':
      return'Mixed'
  elif gender_string == 'h':
      return'Herren'
  elif gender_string == 'd':
      return'Damen'
  elif gender_string == 'u':
      return'Jugend'
  elif gender_string == 'uw':
      return'Jugend-Damen'
  elif gender_string == 'um':
      return'Jugend-Herren'
  elif gender_string == 'uem':
      return'Senioren-Herren'
  elif gender_string == 'uew':
      return'Senioren-Damen'
  elif gender_string == '4x4_d':
      return'4x4-Damen'
  elif gender_string == '4x4_h':
      return'4x4-Herren'
  elif gender_string == '4x4_m':
      return'4x4-Mixed'
  elif gender_string == '4x4_um':
      return'4x4-Jugend-Herren'
  elif gender_string == '4x4_uw':
      return'4x4-Jugend-Damen'
  
  elif gender_string == '4x4_u':
      return'4x4-Jugend-Mixed'
  else:
      return'Sonder'

cups_from_db = []
webpage_not_found = 0
driver2x2 = createDriver()
driver4x4 = createDriver()
messageBot = MessageBot()

def main():
  global cups_from_db
  setupDB()
  while True:
    tempSaveDbCups(db.getCupsFromDb())
    soup = getSoup()
    cups_found = iterateOverSoup(soup)
    compareHtmlAndDb(cups_found)


def iterateOverSoup(soup: list):
  global webpage_not_found
  try:
    cups_found = []
    for cup_html in soup:
      inform = 1
      cup_name = cup_html['class'][0]
      start = 'series='
      gender_string = find_gender(cup_name.replace(start, ''))
      date = cup_html.find('td', class_="date").get_text()
      category = cup_html.find('span', class_="category-shorthandle").get_text()
      name = cup_html.find('a').get_text()
      players = cup_html.find('td', class_="players").get_text()
      
      for l in cup_html.findAll('a'):
        link = 'https://www.beachvolleyball.nrw' + l.get('href')
      cups_found.append(Cup(gender_string, date, category, name, players, link, inform))

    if len(cups_found) > 0:
      webpage_not_found = 0

    return cups_found

  except IndexError as e:
    print(e)
    print('Cup that caused the IndexError: \n', cup_html.prettify())
    return []

def tempSaveDbCups(db_cups: CursorResult):
  global cups_from_db
  for row in db_cups:
    cups_from_db.append(Cup(row['gender'], row['date'], row['category'],
                   row['name'], row['players'], row['link'], row['inform']))

def getSoup():
  global webpage_not_found
  
  if webpage_not_found > 10:
      print('Could not find webpage for the 10 attempt!')
      time.sleep(172800)
      messageBot.sendPrivateMessage("The Bot could not reach the webpage beachvolleyball.nrw after the tenth attempt!")

  try:
    driver2x2.get('https://www.beachvolleyball.nrw/?series=&tournamentsPage=1&tournamentsLimit=800')
    driver4x4.get("https://www.beachvolleyball.nrw/?series=&tournamentsLimit=800&tournamentsPage=1&tt=4x4")
    WebDriverWait(driver2x2, 10).until(EC.visibility_of_element_located(
          (By.CSS_SELECTOR, ".table-tournaments.table.table-hover")))
          
    WebDriverWait(driver4x4, 10).until(EC.visibility_of_element_located(
          (By.CSS_SELECTOR, ".table-tournaments.table.table-hover")))

  except Exception as e:
    print("Was not able to to retrieve Webpage, will try again in 5 Minutes.")
    print(e)
    webpage_not_found +=  1
    time.sleep(300)

  soup2x2 = BeautifulSoup(driver2x2.page_source, 'lxml').find_all(
  "tr", class_=lambda value: value and value.startswith("series"))
  soup4x4 = BeautifulSoup(driver4x4.page_source, 'lxml').find_all(
  "tr", class_=lambda value: value and value.startswith("series"))

  return soup2x2 + soup4x4

def compareHtmlAndDb(html_cups):
  global messageBot
  global cups_from_db
  didFindCup = False
  for html_cup in html_cups:
    if html_cup not in cups_from_db:
      didFindCup = True
      print('Found new Cup!')
      db.insertCupToDb(html_cup)
      messageBot.sendMessage(f'{html_cup.link} \nNeuer {html_cup.category} {html_cup.gender}-Cup in {html_cup.name} am {html_cup.date} \nAngemeldet sind : {html_cup.players} Teams \n')
      time.sleep(2)
      
  if didFindCup == False:
    print('Was not able to find new cups at: ', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '. Will try again in 30 Minutes')
    time.sleep(1800)
time.sleep(10)


main()