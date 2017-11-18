import json,requests,re,warnings
import numpy as np
import scipy.stats as st
import pandas as pd
import urllib.request as scrap
from bs4 import BeautifulSoup

class tolerance:
	def __init__(self,symbol,interval,confidence,invest,start,end):
		self.config = {"invest":invest, "confidence":confidence}
		urlData = "https://kitecharts.zerodha.com/api/chart/%s/%s?public_token=b1e66b02b4e0f36db455a25bb02976f1&user_id=ZP2572&api_key=kitefront&access_token=a1KHa5by0HUQ3xaR8cRXYMxJeUeLqWH0&from=%s&to=%s" % (symbol, interval, start, end) 
		webURL = requests.get(urlData)
		self.JSON_object = json.loads(webURL.text)
	
	def getTolerance(self):
		close = []
		change = []
		try:
			for candle in self.JSON_object["data"]["candles"]:
				close.append(candle[4])
			for a,b in zip(close[::1],close[1::1]):
			    change.append(round(b-a,2))
			minmax = st.norm.interval(float(self.config["confidence"]), np.mean(close), np.std(close))
			mytolerance = st.norm.interval(float(self.config["confidence"]), np.mean(change), np.std(change))
			mytolerance = (round(mytolerance[0],2),round(mytolerance[1],2))
			totalstock = int(self.config["invest"])/close[-1]
			maxloss = totalstock * abs(mytolerance[0])
			maxprofit = totalstock * mytolerance[1]
			totalloss = int(self.config["invest"]) + (totalstock * mytolerance[0])
			totalprofit = int(self.config["invest"]) + maxprofit
			return json.dumps({
				"maxloss": round(maxloss,2),
				"maxprofit": round(maxprofit,2), 
				"totalloss": round(totalloss,2), 
				"totalprofit": round(totalprofit,2), 
				"confidence":self.config["confidence"], 
				"buy": round(minmax[0],2), 
				"sell": round(minmax[1],2)
			})
		except:
			return ''