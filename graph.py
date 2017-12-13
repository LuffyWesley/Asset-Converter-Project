import plotly.offline as py
import plotly.graph_objs as go
import urllib
import json


def safeGet(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None


def getAlphaVantage2():
    baseurl = 'https://www.alphavantage.co/query?'
    method = 'function=TIME_SERIES_DAILY_ADJUSTED'
    outputSize = "outputsize=compact"
    x = input("Enter the stock you are looking to purchase").upper()
    symbol = 'symbol=' + x
    api_key = 'apikey=JY174YSHZ5DCU0FS'
    request = baseurl + method + "&" + outputSize + "&" + symbol + "&" + api_key
    temp = safeGet(request).read()
    finalData = json.loads(temp)
    return finalData


def plotlyGraph():
    data = getAlphaVantage2()
    for x in data:
        for y in data[x]:
            if y == '1. Information':
                title = data[x][y]
            if y == '2. Symbol':
                symbol = data[x][y]

    Xdata = []
    for x in data:
        for y in data[x]:
            Xdata.append(y)
    Xdata = Xdata[5:]
    high = []
    for x in data:
        for y in data[x]:
            temp = data[x]
            for z in temp[y]:
                if z == '2. high':
                    high.append(temp[y][z])
    low = []
    for x in data:
        for y in data[x]:
            temp = data[x]
            for z in temp[y]:
                if z == '3. low':
                    low.append(temp[y][z])
    close = []
    for x in data:
        for y in data[x]:
            temp = data[x]
            for z in temp[y]:
                if z == '4. close':
                    close.append(temp[y][z])
    trace0 = go.Scatter(
        x=Xdata,
        y=high,
        name='Highest Price',
        line=dict(color='rgb(22,96,167', width=2, dash='dot')
    )
    trace1 = go.Scatter(
        x=Xdata,
        y=low,
        name='Lowest Price',
        line=dict(color='rgb(22,96,167', width=2, dash='dot')
    )
    trace2 = go.Scatter(
        x=Xdata,
        y=close,
        name='Closing Price',
        line=dict(color='rgb(205,12,24', width=2, dash='dash')
    )
    data = [trace0, trace1, trace2]
    layout = dict(
        title=title + " for " + symbol,
        xaxis=dict(title='Dates'),
        yaxis=dict(title='Stock Price'),
    )
    # py.init_notebook_mode(connected=True)
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='finalGraph.html')


plotlyGraph()
