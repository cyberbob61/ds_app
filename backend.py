#!/usr/bin/python3.7
import datetime
#some feature
import urllib.request
#1####import requests
from operator import itemgetter
from flask import Flask, render_template, Response, request, redirect, url_for
#import mysql.connector
#from mysql import connector
import mysql
#from __future__ import print_function
#from mysql.connector import errorcode

app = Flask(__name__)

def _time():
    return datetime.datetime.now()
    #return (datetime.datetime.now() - datetime.timedelta(days = 10))

def get_today():
    today = f"{_time():%B %d %Y}"
    return today

def get_yesterday_str():
    yesterday = f"{_time() - datetime.timedelta(days = 1):%B %d %Y}"
    return yesterday

def get_yesterday_int():
    yesterday = f"{_time() - datetime.timedelta(days = 1):%m %d %Y}"
    return yesterday

def get_year_ago_str():
    year_ago = f"{_time() - datetime.timedelta(days = 365):%B %d %Y}"
    return year_ago

def get_year_ago_int():
    year_ago = f"{_time() - datetime.timedelta(days = 365):%m %d %Y}"
    return year_ago


def get_weather_link(day, month, year):
    city = 2123260 #Saint-Petersburg
    result = f"https://www.metaweather.com/api/location/{city}/{year}/{month}/{day}/"
    return result

def get_link_yesterday():
    return get_weather_link(
                get_yesterday_int().split(' ')[1],
                get_yesterday_int().split(' ')[0],
                get_yesterday_int().split(' ')[2])

def get_link_year_ago():
    return get_weather_link(
                get_year_ago_int().split(' ')[1],
                get_year_ago_int().split(' ')[0],
                get_year_ago_int().split(' ')[2])

@app.route("/")
def index():
    return ('hello')

@app.route("/log")
def log():
    today = get_today()
    yesterday = get_yesterday_str()
    link_yesterday = get_link_yesterday()
    year_ago = get_year_ago_str()
    link_year_ago = get_link_year_ago()

    return render_template('log.html',
            today = today,
            yesterday = yesterday,
            year_ago = year_ago,
            link_yesterday = link_yesterday,
            link_year_ago = link_year_ago,
            )

@app.route("/a")
#def get_page_a():
    #url = get_link_yesterday()
    #request = urllib.request.Request(url)
    #with urllib.request.urlopen(request) as response:
    #    the_page = response.read()
    ##filter_list = ['min_temp', 'max_temp', 'the_temp', 'humidity']
    #res = list(itemgetter(*filter_list)(the_page[0]))
    #return 'test'

def dbinit():
    cnx = mysql.connector.connect(
            user='admin',
            passwd='ughLt6RnWOr0gCODgIEm1XZCVvGNxIJutfdLSA10',
            host='db-1.cqzzgt2mptdj.us-east-2.rds.amazonaws.com')
    cursor = cnx.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS weatherapp;")
    cursor.execute("USE weatherapp;")
    cursor.execute("SET sql_notes = 0;")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS yesterday (
            id BIGINT(64) NOT NULL,
            min_temp FLOAT(8),
            max_temp FLOAT(8),
            the_temp FLOAT(8),
            humidity SMALLINT(2))
            ''')
    cursor.execute("SET sql_notes = 1;")

    cursor.execute("SET sql_notes = 0;")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS year_ago (
            id BIGINT(64) NOT NULL,
            min_temp FLOAT(8),
            max_temp FLOAT(8),
            the_temp FLOAT(8),
            humidity SMALLINT(2))
            ''')
    cursor.execute("SET sql_notes = 1;")


def dbinsert(id, min_temp, max_temp, the_temp, humidity):
    cnx = mysql.connector.connect(
            user='admin',
            passwd='ughLt6RnWOr0gCODgIEm1XZCVvGNxIJutfdLSA10',
            host='db-1.cqzzgt2mptdj.us-east-2.rds.amazonaws.com',
            database='weatherapp')
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO yesterday (id, min_temp, max_temp, the_temp, humidity) VALUES (%s, %s, %s, %s, %s)",(id, min_temp, max_temp, the_temp, humidity))
    cnx.commit()

def get_items_from_url_yesterday():
    import json
    url = get_link_yesterday()
    request = urllib.request.Request(url)
    with urllib.request.urlopen(request) as response:
        response = response.read()
    dic = json.loads(response)
    for items in dic:
        remove_key = items.pop("weather_state_name", None)
        remove_key = items.pop("weather_state_abbr", None)
        remove_key = items.pop("wind_direction_compass", None)
        remove_key = items.pop("created", None)
        remove_key = items.pop("applicable_date", None)
        remove_key = items.pop("wind_speed", None)
        remove_key = items.pop("wind_direction", None)
        remove_key = items.pop("air_pressure", None)
        remove_key = items.pop("visibility", None)
        remove_key = items.pop("predictability", None)
    return dic

def get_items_from_url_year_ago():
    import json
    url = get_link_year_ago()
    request = urllib.request.Request(url)
    with urllib.request.urlopen(request) as response:
        response = response.read()
    dic = json.loads(response)
    for items in dic:
        remove_key = items.pop("weather_state_name", None)
        remove_key = items.pop("weather_state_abbr", None)
        remove_key = items.pop("wind_direction_compass", None)
        remove_key = items.pop("created", None)
        remove_key = items.pop("applicable_date", None)
        remove_key = items.pop("wind_speed", None)
        remove_key = items.pop("wind_direction", None)
        remove_key = items.pop("air_pressure", None)
        remove_key = items.pop("visibility", None)
        remove_key = items.pop("predictability", None)
    return dic

def dbinitinsert():
    cnx = mysql.connector.connect(
            user='admin',
            passwd='ughLt6RnWOr0gCODgIEm1XZCVvGNxIJutfdLSA10',
            host='db-1.cqzzgt2mptdj.us-east-2.rds.amazonaws.com',
            database='weatherapp')
    cursor = cnx.cursor()
    list1 = get_items_from_url_yesterday()
    for dict1 in list1:
        placeholders = ', '.join(['%s'] * len(dict1))
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in dict1.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in dict1.values())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('yesterday', columns, values)
        #print (sql)
        cursor.execute(sql)

    list2 = get_items_from_url_year_ago()
    for dict2 in list2:
        placeholders = ', '.join(['%s'] * len(dict1))
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in dict2.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in dict2.values())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('year_ago', columns, values)
        #print (sql)
        cursor.execute(sql)
    cnx.commit()



if __name__ == '__main__':
    dbinit()
    #print(get_items_from_url())a
    #dbfill()
    dbinitinsert()
    ##filter_list = ['min_temp', 'max_temp', 'the_temp', 'humidity']
    #res = list(itemgetter(*filter_list)(the_page[0]))
    #return 'test'
    #print (content)
    #app.run(host="0.0.0.0", port=80, debug=False)
