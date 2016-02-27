# By Adam Chang, Richard Zhou, and Victor Zhou
# Fetches stock prices for a company I guess

import urllib.request
import os
import datetime
import xml.etree.ElementTree as ET


class getStocks:
    """Gets the stock data from Yahoo! Finance."""

    startYear = 2013  # this is as far back as data goes (exclusive)
    # replace the * with specific info one desires (date, closing price, etc.)
    url1 = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22"
    url2 = "%22%20and%20startDate%20%3D%20%22"
    url3 = "%22%20and%20endDate%20%3D%20%22"
    url4 = "%22&diagnostics=false&env=store://datatables.org/alltableswithkeys"
    # between 1,2 is ABCD stock name
    # betweeen 2,3 is start date
    # between 3,4 is end date

    def __init__(self):
        self.today = datetime.datetime.today()
        self.compName = "AAPL"  # default it to Apple
        self.url = ""
        self.years = list()   # split up the query
        self.parsedRaw = list()  # holds the parsed xml data
        self.parsed = list()    # holds adjusted values (for split, etc)
        self.ticks = list()   # holds the names of the companies
        self.scalar = 1  # this is the splitting factor

        # splitting it up into 1 year chunks
        for i in range(self.today.year, getStocks.startYear, -1):
            self.years.append(i)

        # all the file-writing stuff
        os.makedirs("stockData", exist_ok=True)
        self.file = open("tickers.txt", "r")  # opens the file
        for name in self.file:
            if name[-1] == "\n":
                self.ticks.append(name[:-1])   # add names to array omitting the newline
            else:
                self.ticks.append(name)
        self.file.close()

    def giveName(self, abcd):
        """Give the function the name of the company."""
        self.compName = str(abcd)

    def writeToFile(self):
        """Writes the data into a CSV file under the name of the company."""
        os.makedirs(str("stockData/" + self.compName), exist_ok=True)
        writeData = open(str("stockData/" + self.compName + "/px.csv"), "w")
        for j in testing.parsed:
            # writes a string with the date and the closing price
            writeData.write(str(j[0] + ',' + str(j[1]) + '\n'))
        writeData.close()

    def getData(self):
        """Makes the queries to Yahoo! API."""

        # clear current parsed data for the new ones
        self.parsed.clear()
        self.parsedRaw.clear()
        self.scalar = 1

        # parsing data in 1 year chunks
        for i in range(len(self.years)):
            # the chunk data
            dateEnd = str(self.years[i]) + "-12-31"
            dateStart = str(self.years[i]) + "-01-01"

            # update url
            self.url = getStocks.url1 + self.compName + getStocks.url2 + dateStart + getStocks.url3 + dateEnd + getStocks.url4

            # the actual parsing
            page = urllib.request.urlopen(self.url)
            parsedXML = ET.parse(page)
            page.close()

            # getting the numbers
            stockData = parsedXML.getroot()

            # speeds up null runs
            if not len(stockData[0]):
                return

            # getting every day's info
            for k in range(len(stockData[0])):
                # gonna clean up the date
                stockDate = str(stockData[0][k][0].text)
                stockDate = stockDate.replace('-', '')

                # checking if we need to adjust for split
                if len(self.parsedRaw) and self.parsedRaw[-1][1] * 1.25 < float(stockData[0][k][1].text):
                    # update scalar with opening price (the most accurate)
                    self.scalar *= (self.parsedRaw[-1][1] / float(stockData[0][k][1].text))

                # add a list containing the date and stock closing price
                self.parsed.append(list([str(stockDate), float(
                                   stockData[0][k][4].text) * self.scalar]))
                self.parsedRaw.append(list([str(stockDate), float(stockData[0][k][4].text)]))

# TESTING

testing = getStocks()
# making primary folder if it doesn't exist and select it

for i in testing.ticks:   # get data for each name
    testing.giveName(i)
    testing.getData()
    testing.writeToFile()
