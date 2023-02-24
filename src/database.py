import sqlite3
import os
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import create_engine

metaData = MetaData()

engine = create_engine('sqlite:///db/cups.db', echo=True)

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
    if os.path.exists("db/cups.db"):
        print("Database was already created!")
        return

    # Create Database and connect via
    sqlite3.connect("db/cups.db")

    # creates the Tables in the SQLite DB
    metaData.create_all(engine)


def getUserTable():
    return db_cups


def getDbConnection():
    return engine