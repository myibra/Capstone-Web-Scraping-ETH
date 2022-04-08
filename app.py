from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data/usd?start_date=2020-01-01&end_date=2021-06-30#panel')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table')
all = table.find_all('tr')

row_length = len(all)

temp = [] #initiating a list 

for i in range(1, row_length):
    
    #row
    row = table.find_all('tr')[i]

    #Date
    Date = row.find_all('th')[0].text
    
    #Volume
    Volume = row.find_all('td')[1].text
    
    temp.append((Date, Volume))

temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp, columns=('Date', 'Volume'))

#insert data wrangling here
data['Volume'] = data['Volume'].str.replace('\n','')
data['Volume'] = data['Volume'].str.replace('$','', regex=True)
data['Volume'] = data['Volume'].str.replace(',','')
data['Volume'] = data['Volume'].astype(int)
data['Date'] = data['Date'].astype('datetime64[ns]')
data = data.set_index('Date')
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{data["Volume"].mean().round(2):,.2f}' #be careful with the " and ' 

	# generate plot
	ax = data.plot(kind='line', ylabel='Volume(100 milyar USD )',figsize = (10,7)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)