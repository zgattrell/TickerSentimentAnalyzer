from flask import Flask
from flask import render_template
import StockPredictor
from flask import request
import requests
import json

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("/index.html")

@app.route("/search", methods = ['GET'])
def search():

    if request.method == 'GET':
        #Load the search query into a variable
        ticker = request.args.get("ticker")
        #use to the yahoo finance api to get data on the stock
        j = getTickerData(ticker)
        #Use the stock name gather from the yahoo finance api to search for sentiment
        stockName = j['quoteType']['shortName']
        sentimentChartUrl = StockPredictor.getSentimentChart(ticker, stockName)


        return render_template("search.html",
                               c_Name=stockName,
                               c_Ticker=ticker,
                               c_Price=j['summaryDetail']['ask']['raw'],
                               c_Sector=j['assetProfile']['sector'],
                               c_Industry=j['assetProfile']['industry'],
                               c_Description=j['assetProfile']['longBusinessSummary'],
                               c_EmployeeNumber=j['assetProfile']['fullTimeEmployees'],
                               c_Sent_Chart = sentimentChartUrl
                               )
        #return "Sentiment for " + ticker + " is " + str(StockPredictor.getTickerSentimentTest(ticker)) + str(j['quoteType']['shortName'])

    return "Ticker Not Found!"

def getTickerData(arg1):
    # connect to the rapidapi's version of the yahoo finance api
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-profile"

    querystring = {"symbol": arg1, "region": "US"}

    headers = {
        'x-rapidapi-key': "782cbae115mshc02532c0c330f34p192743jsn123f582f2223",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return json.loads(response.text)


def getApp():
    return app


if __name__ == "__main__":
    app.run(debug=True)
