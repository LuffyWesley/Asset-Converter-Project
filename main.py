import webapp2
import urllib2
import json
import jinja2

import os
import logging

# Enter your own API Key from http://www.alphavantage.co/support/#api-key
ALPHAVANTAGE_KEY = ''

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'], autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("In MainHandler")

        template_values = {'page_title': "Asset Converter"}
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


class GreetResponseHandlr(webapp2.RequestHandler):
    def post(self):
        vals = {}
        from_input = self.request.get('from_input')
        to_input = self.request.get('to_input')
        quantity_input = self.request.get('quantity_input')
        vals['page_title'] = "Asset Converter"

        if from_input and to_input and quantity_input:
            from_input = self.request.get('from_input')
            to_input = self.request.get('to_input')
            quantity_input = self.request.get('quantity_input')
            vals['from_input'] = from_input
            vals['to_input'] = to_input
            vals['quantity_input'] = quantity_input

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
