import FlaskServer
import RedditUtils
import pandas as pd
import datetime as datetime
import time
from flask import url_for
from prawcore.exceptions import Forbidden
import matplotlib.pyplot as plt

def load_Nasdaq():
    nasdaq = open("nasdaqtraded.txt")
    #Create the dataframe for all the data
    df = pd.DataFrame(
        columns=['Post_ID', 'Time_Created', 'Ticker', 'Post_Title', 'Post_Comments', 'Overall_Post_Sentiment'])
    #reads through list of nasdaq traded stocks and pulls the ticker and stock name from the file
    #in the future do more to parse stock name
    for line in nasdaq:
        ticker = line.split("|")[1]
        stockName = line.split("|")[2]
        #Compile a data from collecting posts based on searching reddit for both ticker and stockname
        #df = df.append([RedditUtils.getPost(ticker), RedditUtils.getPost(stockName)]
        try:
            df2 = RedditUtils.getDataframe("wallstreetbets", ticker, stockName)
            df = df.append(df2)
            print(df2.to_string)
        except:
            print("Forbidden")

        print("$" + ticker + " - " + stockName)
    nasdaq.close()
    return df

def getTickerSentimentTest(arg1):
    df = load_Nasdaq()
    print(df.to_string())
    df.to_csv(r'export_dataframe.csv', index=False, header=True)
    #df = pd.read_csv("export_dataframe.csv")
    #print(df.to_string())
    ticker_sentiment = df[['Ticker', 'Overall_Post_Sentiment']]

    tickercor = ticker_sentiment[ticker_sentiment['Ticker'] == arg1]
    return tickercor['Overall_Post_Sentiment'].mean()

#Takes a string as a stock ticker and returns a link to a image file of the chart
def getSentimentChart(arg1, arg2):

    df = RedditUtils.getDataframe("wallstreetbets", arg1, arg2)
    ticker_sentiment = df[['Time_Created', 'Overall_Post_Sentiment']]
    date = datetime.datetime.fromtimestamp(1607912895)
    print(date.date())

    print(ticker_sentiment.to_string())
    #create the scatter plot
    scatter_Plot = ticker_sentiment.plot.scatter(x='Time_Created',
                                                 y='Overall_Post_Sentiment')

    fig = scatter_Plot.get_figure()
    filename = arg1 + str(int(time.time())) + ".png"
    filepath = "venv/static/" + filename
    fig.savefig(filepath)
    filepath = url_for('static', filename=filename)
    return filepath

def main():
    FlaskServer.getApp().run()

if __name__ == "__main__":
    main()
