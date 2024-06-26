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
        wtext_advice = 'It might not be a bad idea to stay at home today...'
    else:
        wtext_advice = "That's Pretty Clear. How about going on a walk?"

    if wdata['pop'] > 0.5:
        wtext2_advice = "Make sure to carry an ambrella if you're going out."
    else:
        wtext2_advice = "There shouldn't be any rain, unless something makes Indra angry again!"

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
    x = np.linspace(-1, 1, 50)
    y = x*math.tan(theta)
    plt.plot(x, y, '--')

    # To plot X and Y axis
    plt.plot(x, np.zeros(len(x)), color='k')
    plt.plot(np.zeros(len(y)), y, color='k')
    plt.text(1, 0, 'East')
    plt.text(0, 1, 'North')
    plt.text(0, -1, 'South')
    plt.text(-1, 0, 'West')

    def sgn(val):
        if x > 0 :
            return +1
        elif x < 0 :
            return -1
        else: 
            return 0

    # To elaborate the direction of wind
    arrow = [sgn(math.cos(x)), sgn(math.sin(x))]
    # Arrow
    plt.arrow(0, 0, arrow[0], arrow[1], width=x.max() /10, color='k')
    plt.title("Wind direction chart")
    plt.show()

#Boxplot of temperature variation
def temp_variance(data):
    plt.boxplot(data.loc[:, 0], vert=False)
    plt.xticks(data.loc[:, 0])
    plt.title("Temperature variance chart")
    plt.show()


#To ellaborate the temperture gap between maximum, minimum and the current temperature
def temp_distribution(temp):
    maxima = temp.values[3] - temp.values[0]
    minima = abs(temp.values[2] - temp.values[0])
    x = np.linspace(0, 2 * math.pi, 100)

    y = []
    
    for i in x:
        if i > math.pi:
            amp = minima
        else:
            amp = maxima

        y.append(amp * math.sin(i))
    plt.plot(x, np.zeros(len(x)))
    plt.plot(x, y)
    plt.yticks(list([float(max(y)), float(min(y))]), [str(temp.values[3]) + '(max)', str(temp.values[2]) + '(min)'])
    plt.text(0,0,'Current temperature(' + str(temp.values[0]) +')')
    plt.grid()
    plt.title("Temperature distribution")
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

    temp_variance(temp_data)
    temp_distribution(temp_data)
    wind_dir(wind_data)
