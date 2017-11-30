import urllib.parse
import urllib.request
import urllib.error
import json

'''
Below is a sample of currency code's you can use for this program.

United Arab Emirates = AED
United States = USD
Taiwan = TWD
Kenya = KES
Bitcoin = BTC
Ethereum = ETH
Litecoin = LTC
'''


# Calls the API and accepts user input for currencies to convert.
def getAlphaVantage():
    baseurl = 'https://www.alphavantage.co/query?'
    method = 'function=CURRENCY_EXCHANGE_RATE'
    from_currency = 'from_currency=' + (input("\nEnter the currency you are transferring from: ").upper())
    to_currency = 'to_currency=' + (input("Enter the currency you are transferring to: ").upper())
    api_key = 'apikey=JY174YSHZ5DCU0FS'
    request = baseurl + method + "&" + from_currency + "&" + to_currency + "&" + api_key
    json_string = urllib.request.urlopen(request).read()
    data = json.loads(json_string)
    return data


# Outputs data of interest.
def printAlphaVantage():
    get = getAlphaVantage()
    from_code = get['Realtime Currency Exchange Rate']['1. From_Currency Code']
    from_name = get['Realtime Currency Exchange Rate']['2. From_Currency Name']
    to_code = get['Realtime Currency Exchange Rate']['3. To_Currency Code']
    to_name = get['Realtime Currency Exchange Rate']['4. To_Currency Name']
    quantity = input("How much of %s (%s) would you like to convert to %s (%s): " % (from_name, from_code, to_name, to_code))
    rate = float(get['Realtime Currency Exchange Rate']['5. Exchange Rate'])*float(quantity)
    refresh = get['Realtime Currency Exchange Rate']['6. Last Refreshed']
    time_zone = get['Realtime Currency Exchange Rate']['7. Time Zone']

    print("The current exchange rate for %s %s (%s) is %s %s (%s). This information was last updated on %s %s.\n" % (
        quantity, from_name, from_code, rate, to_name, to_code, refresh, time_zone))


# Handles HTTP errors.
def getAlphaVantageSafe():
    try:
        return printAlphaVantage()
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print("The server couldn't fulfill the request.")
            print("Error code: ", e.code)
        elif hasattr(e, 'reason'):
            print("We failed to reach a server")
            print("Reason: ", e.reason)
        return None


print("Welcome to Wesley's real-time exchange rate for any pair of digital currency or physical currency.")
getAlphaVantageSafe()

# Will ask user if they want to convert another pair of currency. Accepts yes, yeah, y etc for continuation.
while True:
    another = (input("Do you want to convert another pair of currency? (Y/N): ")).upper()
    if another[0] == 'Y':
        getAlphaVantageSafe()
    else:
        break
