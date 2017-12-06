# Asset-Converter
This program is an asset converter which will allow you to see what your current's assets value would be in another asset form such as physical currency, digital currency or stocks. 

Alpha Vantage delivers a free API for real time financial data and most used finance indicators in a simple JSON or pandas format. It requires a free API, that can be requested on http://www.alphavantage.co/support/#api-key. You can have a look at all the API calls available in their documentation http://www.alphavantage.co/documentation. 

To get data in python, simply call the object with your API key and get ready for free real-time financial data. The library supports giving its results as JSON dictionaries (default) or as pandas data frame, simply pass the parameter output_format=’pandas’ to change the format of the output for all the API calls. Their JSON output is easily readable and python-parsable. In terms of data, the following are what you can expect to get from the API:
1.	Stock market. Provides real-time and historical equity data. 
2.	Foreign Exchange rates. Provided real-time exchange rate for any pair of digital currency or physical currency. 
3.	Digital/crypto currencies. Provides real-time and historical equity data
4.	Stock technical indicators.
5.	Sector performances. Provides real-time and historical sector performances calculated from S&P500 incumbents. 
