import webapp2
import urllib2
import json
import jinja2

""""
import plotly.ofline as py
import plotly.graph_objs as go
"""""

import os
import logging

# Enter your own API Key from http://www.alphavantage.co/support/#api-key
ALPHAVANTAGE_KEY = ''

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'], autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("In MainHandler")

        template_values = {'page_title': "Currency Converter"}
        template = JINJA_ENVIRONMENT.get_template('website.html')
        self.response.write(template.render(template_values))


def safeGet(requested):
    try:
        logging.info(requested)
        return urllib2.urlopen(requested)
    except urllib2.HTTPError as e:
        logging.info('The server couln\'t fulfill the request.')
        logging.info('Error code: ' + e.code)
    except urllib2.URLError as e:
        logging.info('We failed to reach a server')
        logging.info('Reason: ', e.reason)
    return None


# Calls the API and accepts user input for currencies to convert.
def getAlphaVantage(from_input, to_input):
    baseurl = 'https://www.alphavantage.co/query?'
    method = 'function=CURRENCY_EXCHANGE_RATE'
    from_currency = 'from_currency=' + from_input.upper()
    to_currency = 'to_currency=' + to_input.upper()
    api_key = 'apikey=' + ALPHAVANTAGE_KEY
    requested = baseurl + method + "&" + from_currency + "&" + to_currency + "&" + api_key
    return safeGet(requested)


# Outputs data of interest.
def printAlphaVantage(from_input, to_input, quantity_input):
    get = getAlphaVantage(from_input, to_input)
    json_string = get.read()
    data = json.loads(json_string)
    from_code = data['Realtime Currency Exchange Rate']['1. From_Currency Code']
    from_name = data['Realtime Currency Exchange Rate']['2. From_Currency Name']
    to_code = data['Realtime Currency Exchange Rate']['3. To_Currency Code']
    to_name = data['Realtime Currency Exchange Rate']['4. To_Currency Name']
    quantity = quantity_input
    rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate']) * float(quantity)
    refresh = data['Realtime Currency Exchange Rate']['6. Last Refreshed']
    time_zone = data['Realtime Currency Exchange Rate']['7. Time Zone']

    outcome = (
            "The current exchange rate for %s %s (%s) is %s %s (%s). This information was last updated on %s %s.\n" % (
        quantity, from_name, from_code, rate, to_name, to_code, refresh, time_zone))
    return outcome


""""
def getAlphaVantage2(to_crypto_form):
    baseurl = 'https://www.alphavantage.co/query?'
    method = 'function=DIGITAL_CURRENCY_INTRADAY'
    symbol = 'symbol=' + to_crypto_form
    market = 'market=CNY'
    api_key = 'apikey=' + ALPHAVANTAGE_KEY
    request = baseurl + method + "&" + symbol + "&" + market + "&" + api_key
    temp = safeGet(request).read()
    finalData = json.loads(temp)
    return finalData


def plotlyGraph(to_input):
    data = getAlphaVantage2(to_input)
    for x in data:
        for y in data[x]:
            if y == '1. Information':
                info = data[x][y]
            if y == '2. Digital Currency Code':
                code = data[x][y]

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
                if z == '2b. high (USD)':
                    high.append(temp[y][z])
    low = []
    for x in data:
        for y in data[x]:
            temp = data[x]
            for z in temp[y]:
                if z == '3b. low (USD)':
                    low.append(temp[y][z])
    close = []
    for x in data:
        for y in data[x]:
            temp = data[x]
            for z in temp[y]:
                if z == '4b. close (USD)':
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
        title=info + " for " + code,
        xaxis=dict(title='Dates'),
        yaxis=dict(title='Currency Price'),
    )
    # py.init_notebook_mode(connected=True)
    fig = dict(data=data, layout=layout)
    new = py.plot(fig)
    return new
"""""


class GreetResponseHandlr(webapp2.RequestHandler):
    def post(self):
        vals = {}
        from_input = self.request.get('from_input')
        to_input = self.request.get('to_input')
        quantity_input = self.request.get('quantity_input')
        # to_crypto_form = self.request.get('to_crypto_form')
        vals['page_title'] = "Currency Converter"

        if from_input and to_input and quantity_input:
            from_input = self.request.get('from_input')
            to_input = self.request.get('to_input')
            quantity_input = self.request.get('quantity_input')
            vals['from_input'] = from_input
            vals['to_input'] = to_input
            vals['quantity_input'] = quantity_input
            """""
            if to_crypto_form:
                vals['to_input'] = to_input
                graph = plotlyGraph(to_input)
                vals['graph'] = graph
            """""
            results = printAlphaVantage(from_input, to_input, quantity_input)

            vals['results'] = results

            template = JINJA_ENVIRONMENT.get_template('results.html')
            self.response.write(template.render(vals))
        else:
            template = JINJA_ENVIRONMENT.get_template('website.html')
            self.response.write(template.render(vals))


application = webapp2.WSGIApplication([ \
    ('/results', GreetResponseHandlr),
    ('/.*', MainHandler)
],
    debug=True)
