import sqlite3
import os
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import create_engine

metaData = MetaData()

engine = create_engine('sqlite:///cups.db', echo=False)

db_cups = Table('cups', metaData,
                Column('id', String, primary_key=True),
                Column('gender', String),
                Column('date', String),
                Column('category', String),
                Column('name', String),
                Column('players', String),
                Column('link', String),
                Column('inform', Integer)
                )


def setUp():
    # Check if Database is available
    if os.path.exists("cups.db"):
        print("Database was already created!")
    else:
        # Create Database and connect via
        sqlite3.connect("cups.db")

        # creates the Tables in the SQLite DB
        metaData.create_all(engine)


def getCupsFromDb():
    try:
        c = engine.connect()
        cups =  c.execute(db_cups.select())
        c.close()
    except Exception as e:
        print("Tryining to get Cups From DB...")
        print(e)
    return cups.all()


def insertCupToDb(html_cup): 
    try:
        c = engine.connect()
        c.execute(db_cups.insert().values(id=html_cup.id, gender=html_cup.gender, date=html_cup.date,
                                          category=html_cup.category, name=html_cup.name, players=html_cup.players,
                                          link=html_cup.link, inform=html_cup.inform))
        c.commit()
        c.close()
    except Exception as e:
        print()
        print(e)
        print(html_cup)
        print()
    