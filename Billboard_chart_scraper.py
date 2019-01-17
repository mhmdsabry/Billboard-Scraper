from requests import get
from bs4 import BeautifulSoup
from datetime import timedelta,date
from time import time,sleep
from IPython.core.display import clear_output
import pandas as pd 
from warnings import warn
from random import randint
#list to store scraped data
ArtistName = []
SongName = []
Rank = []
WeeksOnChart = []
WeeksAsNumberOne = []


start_time = time()
requests_counter = 0

    #functions generate specific duration of dates used in url
def date_range(start_date,end_date):
        for i in range(0,int((end_date - start_date).days),7):
            yield start_date + timedelta(i)

for single_date in date_range(date(2015,1,3),date(2019,1,12)):
    
    request = get('https://www.billboard.com/charts/hot-100/'+single_date.strftime("%Y-%m-%d"))
    
    #mintoring requests #1.(check status code) #2.(claculate request speed)) #3.(check request couner not exceed limit)
    sleep(randint(8,30))
    requests_counter += 1
    #1
    if request.status_code!=200:
        warn('Request : {} status code : {}'.format(requests_counter,request.status_code))
    else:
        
       #2
       requests_time = time() - start_time
       print('Request : {} Request speed : {}'.format(requests_counter,requests_counter/requests_time))
       clear_output(wait=True)
       
       #3
       if requests_counter > 211:
           warn('Request number exceed the determinded limit')
           break
        
       #Parse Html Content
       html_parser = BeautifulSoup(request.text,'html.parser')

       #for number one song ,because it has different layout from others
       artist_1 = html_parser.find("div","chart-number-one__artist").text
       ArtistName.append(artist_1)
       song_1 = html_parser.find("div","chart-number-one__title").text
       SongName.append(song_1)
       weeks_on_chart_1 = int(html_parser.find("div","chart-number-one__weeks-on-chart").text)
       WeeksOnChart.append(weeks_on_chart_1)
    
       #in case of  songs top the charts for first time
       week_as_number_one = html_parser.find("div","chart-number-one__weeks-at-one")
       if  week_as_number_one is not None:
           week_as_number_one =  int(week_as_number_one.text)
           WeeksAsNumberOne.append(week_as_number_one)
       else:
           WeeksAsNumberOne.append(0)
    
       #the rank number was image,so as it's obvious 
       Rank.append(1)
        
        #for other songs in the chart
       item_container = html_parser.find_all("div","chart-list-item")
       for container in item_container:
            artist = container['data-artist']
            ArtistName.append(artist)
            song = container['data-title']
            SongName.append(song)
            rank = int(container['data-rank'])
            Rank.append(rank)
        
            #in case of fresh songs enter the charts
            weeks_on_chart = container.find("div","chart-list-item__weeks-on-chart")
            if weeks_on_chart is not None:
                 weeks_on_chart = int(weeks_on_chart.text)
                 WeeksOnChart.append(weeks_on_chart)
            else:
                WeeksOnChart.append(0)
            
            #Weeks As Number One not for all song image,so as it's obvious  
            WeeksAsNumberOne.append(0)

           #make put data in respentive pandas data frame
            Billboard_Chart = pd.DataFrame({'Artist':ArtistName,'Song':SongName,'Rank':Rank,'Weeks On Chart':WeeksOnChart
                      ,'Weeks On #1':WeeksAsNumberOne})
            Billboard_Chart.to_csv('BillboardChart.csv')
