from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from sqlalchemy import CursorResult
from sqlalchemy.sql import select, insert
from cup import Cup
import database as db
import time
import datetime
import sqlalchemy

def createChromeOptions():
  options = webdriver.ChromeOptions()
  options.add_argument('--ignore-certificate-errors')
  options.add_argument('--incognito')
  options.add_argument('--headless')
  return options


def createDriver():
  return webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=createChromeOptions())


def setupDB():
  db.setUp()
  return db.getDbConnection().connect()

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


def main():
  dbConnection = setupDB()
  db_cups = dbConnection.execute(select([db.getUserTable()]))
  soup = getSoup(db_cups)
  cups_found = iterateOverSoup(soup)
  compareHtmlAndDb(db_cups, cups_found, dbConnection)

cups_from_db = []
no_cups_found_counter = 0
driver2x2 = createDriver()
driver4x4 = createDriver()


def iterateOverSoup(soup: list):
  global no_cups_found_counter
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

    if cups_found.__sizeof__ > 0:
      no_cups_found_counter = 0

    return cups_found

  except IndexError as e:
    print(e)
    print('Cup that caused the IndexError: \n', cup_html.prettify())
    return []


def getSoup(db_cups: CursorResult):
  global no_cups_found_counter
  for row in db_cups:
    cups_from_db.append(Cup(row['gender'], row['date'], row['category'],
                   row['name'], row['players'], row['link'], row['inform']))
  
  while True:
    if no_cups_found_counter > 10:
       print('Send error-message here!')

    try:
      driver2x2.get('https://www.beachvolleyball.nrw/?series=&tournamentsPage=1&tournamentsLimit=800')
      driver4x4.get("https://www.beachvolleyball.nrw/?series=&tournamentsLimit=800&tournamentsPage=1&tt=4x4")
      WebDriverWait(driver2x2, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".table-tournaments.table.table-hover")))
            
      WebDriverWait(driver4x4, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".table-tournaments.table.table-hover")))

    except:
      print("Was not able to to retrieve Webpage, will try again in 5 Minutes.")
      no_cups_found_counter +=  1
      time.sleep(300)

    soup2x2 = BeautifulSoup(driver2x2.page_source, 'lxml').find_all(
    "tr", class_=lambda value: value and value.startswith("series"))
    soup4x4 = BeautifulSoup(driver4x4.page_source, 'lxml').find_all(
    "tr", class_=lambda value: value and value.startswith("series"))

    return soup2x2 + soup4x4

def compareHtmlAndDb(html_cups, db_cups):
  willSendMessage = False
  for html_cup in html_cups:
    if html_cup not in db_cups:
      willSendMessage = True
      print('Found new Cup!')
      insert = db.getUserTable.insert().values(id=html_cups.id, gender=html_cups.gender, date=html_cups.date,
                                          category=html_cups.category, name=html_cups.name, players=html_cups.players, link=html_cups.link, inform=html_cups.inform)
      try:
        result = db.getDbConnection().connect().execute(insert)
      except sqlalchemy.exc.IntegrityError as e:
        print()
        print(e)
        print(html_cup)
        print()
      
  if willSendMessage == True:
    # SEND MESSAGE HERE
    print('Should send message here')
  else:
    print('Was not able to find new cups at: ', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '. Will try again in 30 Minutes')
    time.sleep(1800)
time.sleep(10)


    

main()