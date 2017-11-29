'''
Created on Nov 28, 2017

@author: trice
'''
import unittest
import ephem
import plotly.plotly as py
import plotly.graph_objs as go

import math
import time
from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 
import matplotlib

import datetime
sun = ephem.Sun()
obs = ephem.Observer()
obs.lat, obs.long = '35.7796', '-78.6382' # Raleigh
obs.elevation = 31

def sunrise(location, date, horizon = '-0:34'):
    return sr('rise', location, date, horizon)

def sunset(location, date, horizon = '-0:34'):
    return sr('set', location, date, horizon)

def sr(event, location, date, horizon = '-0:34'):
    ''' code sharing, its a good thing '''
    location.date = date
    location.horizon = horizon
    sun.compute(location)
    if 'rise' in event:
        sr = location.next_rising(sun)
    elif 'set' in event:
        location.date += (ephem.hour * 6)
        sr = location.next_setting(sun)
    return sr.datetime()

def risesetdeltabycity2(lat, lon, city):
    start='2017-11-30'
    end='2017-12-31'
    df = pd.DataFrame(index=pd.date_range(start=start, end=end, freq='D', tz="UTC"))

    obs = ephem.Observer()
    obs.lon, obs.lat = lon, lat
    obs.horizon = '-0:34'  # match US Naval Observatory
    obs.pressure = 0.0

    for riseset in ['rise', 'set']:
        df[riseset] = df.index.map(lambda d: sr(riseset, obs, d))
        df["sun%s" % riseset] = (df[riseset] - df.index) / np.timedelta64(1, 'us') / 1000000 / 60 / 60

    print(df.to_string())

    ax = plt.figure(figsize=(7,4), dpi=300).add_subplot(111)
    ax.set_xlabel("2017")
    ax.set_ylabel(r' hour (UTC)')
    df.plot(ax=ax, style='-')
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    dfmt = mdates.DateFormatter('%b')

    ax.xaxis.set_major_formatter(dfmt)
    ax.xaxis.set_minor_locator(mdates.DayLocator(interval=7))
    ax.xaxis.grid(False, which="minor")
    ax.xaxis.grid(True, which="major")

    equinoxes = ['2017-03-20', '2017-06-21', '2017-09-21', '2017-12-21']
    ymin, ymax = ax.get_ylim()
    ax.vlines(x=equinoxes, ymin=ymin, ymax=ymax + 1, color='r')

    plt.title(city, fontsize=20)
    plt.savefig('%s riseset2.png' % city)
    plt.show()  

def risesetdeltabycity(lat, lon, city):
    start='2016-12-31'
    end='2017-12-31'
    df = pd.DataFrame(index=pd.date_range(start=start, end=end, freq='D', tz="UTC"))

    obs = ephem.Observer()
    obs.lon, obs.lat = lon, lat
    obs.horizon = '-0:34'  # match US Naval Observatory
    obs.pressure = 0.0

    for riseset in ['rise', 'set']:
        df['sun%s' % riseset] = df.index.map(lambda d: sr(riseset, obs, d))
        df['sun%s change' % riseset] = ( (pd.to_datetime(df['sun%s' % riseset]) - pd.to_datetime(df['sun%s' % riseset].shift(1))) / np.timedelta64(1, 'us') / 1000000 ) - 86400.0
        df['sun%s' % riseset] = df['sun%s' % riseset].map(lambda t: t.time())

    print(df.to_string())

    ax = plt.figure(figsize=(7,4), dpi=300).add_subplot(111)
    ax.set_xlabel("2017")
    ax.set_ylabel(r'$\Delta$ seconds')
    df.plot(ax=ax, style='-')
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    dfmt = mdates.DateFormatter('%b')

    ax.xaxis.set_major_formatter(dfmt)
    ax.xaxis.set_minor_locator(mdates.DayLocator(interval=7))
    ax.xaxis.grid(False, which="minor")
    ax.xaxis.grid(True, which="major")


    equinoxes = ['2017-03-20', '2017-06-21', '2017-09-21', '2017-12-21']
    ymin, ymax = ax.get_ylim()
    ax.vlines(x=equinoxes, ymin=ymin, ymax=ymax+1, color='r')

    plt.title(city, fontsize=20)
    plt.savefig('%s.png' % city)  
    plt.show()  

def risesetdeltabylat():
    start='2017-11-30'
    end='2017-12-31'
    df = pd.DataFrame(index=pd.date_range(start=start, end=end, freq='D', tz="UTC"))


    ax = plt.figure(figsize=(7,4), dpi=300).add_subplot(111)
    ax.set_xlabel("2017")
    ax.set_ylabel(r'$\Delta$ seconds')
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    dfmt = mdates.DateFormatter('%b')
    ax.xaxis.set_major_formatter(dfmt)
    ax.xaxis.set_minor_locator(mdates.DayLocator(interval=7))
    ax.xaxis.grid(False, which="minor")
    ax.xaxis.grid(True, which="major")

    for lat in [0,20,40,60,]:
        print lat
        wfmy = ephem.Observer()
        wfmy.lon, wfmy.lat = str(-78.0), str(lat)
        wfmy.horizon = '-0:34'  # match US Naval Observatory
        wfmy.pressure = 0.0

        for riseset in ['rise', 'set']:
            df['sun%s' % riseset] = df.index.map(lambda d: sr(riseset, wfmy, d))
            df[r'%d$\degree$ lat %s' % (lat, riseset)] = ( (pd.to_datetime(df['sun%s' % riseset]) - pd.to_datetime(df['sun%s' % riseset].shift(1))) / np.timedelta64(1, 'us') / 1000000 ) - 86400.0
            df['sun%s' % riseset] = df['sun%s' % riseset].map(lambda t: t.time())

    df.plot(ax=ax, style='-')



    equinoxes = ['2017-03-20', '2017-06-21', '2017-09-21', '2017-12-21']
    ymin, ymax = ax.get_ylim()
    ax.vlines(x=equinoxes, ymin=ymin-6, ymax=ymax+5, color='k')

    plt.title("daily sun rise/set deltas by Latitude", fontsize=20)

    plt.savefig('data.png')  
    plt.show()  
    f.close()
    plt.close()


class Test(unittest.TestCase):

    def dtestbyLat(self):
        risesetdeltabylat()

    def dtestName2(self):
        risesetdeltabycity2('36.0998572',  "-79.7621832", 'Greensboro, NC')
        risesetdeltabycity2('8.94',  "-79.52", 'Panama City, Panama')

    def testName(self):
        risesetdeltabycity('36.0998572',  "-79.7621832", 'Greensboro, NC')
        risesetdeltabycity('8.94',  "-79.52", 'Panama City, Panama')
        risesetdeltabycity('0.0',  "-79.52", 'on the equator')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()