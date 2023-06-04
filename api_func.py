import api_keys

def weather(inp):
    weather = api_keys.weather_report(inp)
    loc = weather.json()['location']['name']
    temp_c = weather.json()['current']['temp_c']
    temp_feel_c = weather.json()['current']['feelslike_c']
    wind_km = weather.json()['current']['wind_kph']
    wind_deg = weather.json()['current']['wind_degree']
    wind_dir = weather.json()['current']['wind_dir']
    des = weather.json()['current']['condition']['text']
    vis_km = weather.json()['current']['vis_km']
    uv = weather.json()['current']['uv']
    hum = weather.json()['current']['humidity']

    print(f"{loc} in {weather.json()['location']['country']} has a temperature of {temp_c:.2f} °C but it feels like {temp_feel_c} °C.\nThe wind is flowing at a speed of {wind_km} km/hr at {wind_deg}° {wind_dir}. Humidity being {hum}%.\nThe weather is {des} with a visibilty of {vis_km} km and a U.V. index of {uv}.")
    return (f"{loc} in {weather.json()['location']['country']} has a temperature of {temp_c:.2f} °C but it feels like {temp_feel_c} °C.\nThe wind is flowing at a speed of {wind_km} kilometres per hour at {wind_deg}° {wind_dir}. Humidity being {hum}%.\nThe weather is {des} with a visibilty of {vis_km} kilometers and a U.V. index of {uv}.")

def news(inp):
    n=[]
    i=0
    k=0
    news = api_keys.news_report(inp)
    while i<3:
        if(news.json()['articles'][i]['title'] != news.json()['articles'][i+1]['title']):
            n.append(news.json()['articles'][i+k]['title'])
        else:
            k+=1
        i+=1
    
    print(n)
    return n