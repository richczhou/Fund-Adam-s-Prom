##By Adam Chang, Richard Zhou, and Victor Zhou
##Fetches stock prices for a company I guess

import urllib.request, os, datetime, xml.etree.ElementTree as ET

class getStocks:
    """Gets the stock data from Yahoo! Finance."""

    startYear = 1970  #this is as far back as data goes (exclusive)
    #note that in url1 one can replace the * with specific info one desires (date, closing price, etc.)
    url1 = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22"
    url2 = "%22%20and%20startDate%20%3D%20%22"
    url3 = "%22%20and%20endDate%20%3D%20%22"
    url4 = "%22&diagnostics=false&env=store://datatables.org/alltableswithkeys"
    #between 1,2 is ABCD stock name
    #betweeen 2,3 is start date
    #between 3,4 is end date

    def __init__(self):
        self.today = datetime.datetime.today()
        self.compName = "AAPL"  #default it to Apple
        self.url = ""
        self.years = []  #split up the query
        self.parsed = [] #holds the parsed xml data

        #splitting it up into 1 year chunks
        for i in range(self.today.year, getStocks.startYear, -1):
            self.years.append(i)

    def giveName(self, abcd):
        """Give the function the name of the company."""
        self.compName = str(abcd)

    def getData(self):
        """Makes the queries to Yahoo! API."""
        
        #clear current parsed data for the new ones
        self.parsed.clear()
        
        #parsing data in 1 year chunks
        for i in range(len(self.years)):
            #the chunk data
            dateEnd = str(self.years[i]) + "-12-31"
            dateStart = str(self.years[i]) + "-01-01"
                
            #update url
            self.url = getStocks.url1 + self.compName + getStocks.url2 + dateStart + getStocks.url3 + dateEnd + getStocks.url4
        
            #the actual parsing
            page = urllib.request.urlopen(self.url)
            parsedXML = ET.parse(page)
            page.close()

            #getting the numbers
            stockData = parsedXML.getroot()

            #speeds up null runs
            if not len(stockData[0]):
                return
            
            #getting every day's info
            for k in range(len(stockData[0])):
                #gonna clean up the date
                stockDate = str(stockData[0][k][0].text)
                stockDate = stockDate.replace('-','')
                
                #add a list containing the date and stock closing price
                self.parsed.append(list([str(stockDate), float(stockData[0][k][4].text)]))


#############| TESTING |####################


testing = getStocks()
#making primary folder if it doesn't exist and select it
os.makedirs("stockData", exist_ok=True)
file = open("tickers.txt", "r") #opens the file

ticks = []    #holds the names
for name in file:
    ticks.append(name[:-1])   #add names to array omitting the newline
file.close()

for i in ticks:   #get data for each name
    testing.giveName(i)
    testing.getData()
    
    #store the files
    os.makedirs(str("stockData/" + i), exist_ok=True)
    writeData = open(str("stockData/" + i + "/px.csv"), "w")
    for j in testing.parsed:
        writeData.write(str(j[0] + ',' + str(j[1]) + '\n'))
    writeData.close()
    
