import pandas as pd
import numpy as np
import math
from datetime import datetime as dt
import matplotlib.pyplot as plt
import requests


#Connects to the openwheather API to get wheather information from openweathermap.org
def api_call(city):

    api_url = "https://api.openweathermap.org/data/2.5/forecast?q="+city\
              +"&units=metric&cnt=1&appid=59c4e3002bb3db21a6de6d8963594d85"
    print('making connection to '+api_url)
    response = requests.get(api_url)
    if response.status_code != 200:
        print('ERROR: '+str(response.status_code) + "\nPlease check the name of the city and make sure you have an "
                                                       "internet connection")
    r = response.json()
    status = response.status_code
    return status , r
#To present the data provided by openweathermap in a structured manner
def weather_data(data):
    main = data['list'][0]['main']
    temp = pd.DataFrame(pd.Series(list(main.values())[0:4], index=list(main.keys())[0:4]))
    weather = data['list'][0]['weather'][0]

    list1 = ['pop', 'visibility']
    for i in list1:
        weather[i] = data['list'][0][i]
    list2 = ['pressure', 'grnd_level', 'humidity']
    for i in list2:
        weather[i] = main[i]
    weather['ground level'] = weather.pop('grnd_level')

    fore_time = data['list'][0]['dt']
    fore_time = dt.fromtimestamp(fore_time)
    wind = data['list'][0]['wind']
    return temp, weather, wind, fore_time


def describe_data(wdata, tdata):
    if wdata['visibility'] < 10000:
        wtext_advice = 'It might not be a bad idea to stay at home today...\n'
    else:
        wtext_advice = "That's Pretty Clear. How about going on a walk?\n"

    if wdata['pop'] > 0.5:
        wtext2_advice = "Make sure to carry an ambrella if you're going out.\n"
    else:
        wtext2_advice = "There shouldn't be any rain, unless something makes Indra angry again!\n"

    wtext1 = str(
        wdata['description'] + '\n' + 'visibility is upto ' + str(wdata['visibility']) + ' meters\t' + 'Humidity is ' +
        str(wdata['humidity']) + '%\n' + wtext_advice)
    wtext2 = 'There is ' + str(wdata['pop'] * 100) + '%' + ' Chance of rain' + '\n' + wtext2_advice

    ttext1 = 'temperature is ' + str(tdata[0].values[0]) + ' right now.'
    ttext2 = 'The highest temperature has been ' + str(tdata[0].values[3]) + '\n' + 'While the minimum has been ' + str(
        tdata[0].values[2]) + '\n'

    return wtext1, wtext2, ttext1, ttext2

def wind_dir(data):
    # converting degrees to radians
    theta = (math.pi / 180) * data['deg']

    # equation of straight line to plot the path of wind
    x = np.linspace(-1,1,50)
    y = np.linspace(-1,1,50)
    # To plot X and Y axis
    plt.plot(x, np.zeros(len(x)), color='k')
    plt.plot(np.zeros(len(y)), y, color='k')
    plt.text(1, 0, 'East')
    plt.text(0, 1, 'North')
    plt.text(0, -1, 'South')
    plt.text(-1, 0, 'West')

    def sgn(val):
        if val > 0 :
            return 1
        elif val < 0 :
            return -1
        else: 
            return 0

    # To elaborate the direction of wind
    a1 = sgn(math.cos(theta))
    a2 = sgn(math.sin(theta))
    arrow = [a1, a2]
    # Arrow
    plt.arrow(0, 0, arrow[0], arrow[1], width=0.01, color='k')
    plt.title("Wind direction chart")
    plt.show()

#Boxplot of temperature variation
def temp_variance(data):
    plt.boxplot(data.loc[:, 0], vert=False)
    plt.xticks(data.loc[:, 0])
    plt.title("Temperature variance chart")
    plt.show()




loop = True
while loop:
    print("Welcome to your weather forecast app\n"
          "Please make sure you have an active internet connection for data to be imported from the web")
    city = str(input("Enter the name of the city(enter 'exit' to exit the software') : "))
    if city == "exit" :
         break

    data_status, api_data = api_call(city)
    while data_status != 200:
        city = str(input('Enter the name of the city: '))
        data_status, api_data = api_call(city)

    temp_data, weather_data, wind_data, forecast_time = weather_data(api_data)
    text1, text2, texta, textb = describe_data(weather_data, temp_data)
    print(texta.title() + '\n' + textb.title())
    print('')
    print(text1.title(),'\n', text2.title())
    input("Press enter to continue...")
    temp_variance(temp_data)
    input("Press enter again to view wind data...")
    wind_dir(wind_data)
