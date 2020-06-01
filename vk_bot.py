import yandex_weather_api
import requests as req
import geocoder

#place = "поселок кичигино"
def get_weather(place="Москва"):
    weather_key = "токен" #токен от яндекс погоды
    geo_key="токен" #токен от геокодера
    #далее парсим геолокацию введенного местоположения
    geo_res = req.get("https://geocode-maps.yandex.ru/1.x",params={"format":"json","geocode":place, "apikey":"токен"})
    geo_data = geo_res.json()
    #далее проверка на количество найденных результатов
    found = geo_data['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found']
    if (found == '0'):
        return False
    else:
        try:
            name_place = geo_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['Components'][-1]['name']
            geo_data = geo_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            geo_lat = geo_data.split()[1] #широта
            geo_lng = geo_data.split()[0] #долгота
            #далее парсим погоду по найденной широте и долготе
            weather_res = req.get("https://api.weather.yandex.ru/v1/forecast", params={"lat":geo_lat,"lon":geo_lng},headers={"X-Yandex-API-Key":weather_key})
            weather_data = weather_res.json()
            temperature = weather_data['fact']['temp']
            return [geo_lat, geo_lng, temperature, name_place]
        except:
            return False
def get_weather_today(place="Москва"):
    weather_key = "токен" #токен от яндекс погоды
    geo_key="токен" #токен от геокодера
    #далее парсим геолокацию введенного местоположения
    geo_res = req.get("https://geocode-maps.yandex.ru/1.x",params={"format":"json","geocode":place, "apikey":"токен"})
    geo_data = geo_res.json()
    #далее проверка на количество найденных результатов
    found = geo_data['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found']
    if (found == '0'):
        return False
    else:
        try:
            name_place = geo_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['Components'][-1]['name']
            geo_data = geo_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            geo_lat = geo_data.split()[1] #широта
            geo_lng = geo_data.split()[0] #долгота
            #далее парсим погоду по найденной широте и долготе
            weather_res = req.get("https://api.weather.yandex.ru/v1/forecast", params={"lat":geo_lat,"lon":geo_lng},headers={"X-Yandex-API-Key":weather_key})
            weather_data = weather_res.json()
            #далее температура(от минимальной до максимальной) утро/день/вечер/ночь
            morning_temperature = [weather_data['forecasts'][0]['parts']['morning']['temp_min'],weather_data['forecasts'][0]['parts']['morning']['temp_max']]
            day_temperature = [weather_data['forecasts'][0]['parts']['day']['temp_min'],weather_data['forecasts'][0]['parts']['day']['temp_max']]
            evening_temperature = [weather_data['forecasts'][0]['parts']['evening']['temp_min'],weather_data['forecasts'][0]['parts']['evening']['temp_max']]
            night_temperature = [weather_data['forecasts'][0]['parts']['night']['temp_min'],weather_data['forecasts'][0]['parts']['night']['temp_max']]
            #далее скорость ветра на утро/день/вечер/ночь
            morning_wind = weather_data['forecasts'][0]['parts']['morning']['wind_speed']
            day_wind = weather_data['forecasts'][0]['parts']['day']['wind_speed']
            evening_wind = weather_data['forecasts'][0]['parts']['evening']['wind_speed']
            night_wind = weather_data['forecasts'][0]['parts']['night']['wind_speed']
            return [morning_temperature, day_temperature, evening_temperature, night_temperature, morning_wind, day_wind, evening_wind, night_wind, name_place]
        except:
            return False
def get_weather_tommorow(place="Москва"):
    weather_key = "токен" #токен от яндекс погоды
    geo_key="токен" #токен от геокодера
    #далее парсим геолокацию введенного местоположения
    geo_res = req.get("https://geocode-maps.yandex.ru/1.x",params={"format":"json","geocode":place, "apikey":"токен"})
    geo_data = geo_res.json()
    #далее проверка на количество найденных результатов
    found = geo_data['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found']
    if (found == '0'):
        return False
    else:
        try:
            name_place = geo_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['Components'][-1]['name']
            geo_data = geo_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            geo_lat = geo_data.split()[1] #широта
            geo_lng = geo_data.split()[0] #долгота

            #далее парсим погоду по найденной широте и долготе
            weather_res = req.get("https://api.weather.yandex.ru/v1/forecast", params={"lat":geo_lat,"lon":geo_lng,"limit":2},headers={"X-Yandex-API-Key":weather_key})
            weather_data = weather_res.json()
            #далее температура(от минимальной до максимальной) утро/день/вечер/ночь
            morning_temperature = [weather_data['forecasts'][1]['parts']['morning']['temp_min'],weather_data['forecasts'][1]['parts']['morning']['temp_max']]
            day_temperature = [weather_data['forecasts'][1]['parts']['day']['temp_min'],weather_data['forecasts'][1]['parts']['day']['temp_max']]
            evening_temperature = [weather_data['forecasts'][1]['parts']['evening']['temp_min'],weather_data['forecasts'][1]['parts']['evening']['temp_max']]
            night_temperature = [weather_data['forecasts'][1]['parts']['night']['temp_min'],weather_data['forecasts'][1]['parts']['night']['temp_max']]
            #далее скорость ветра на утро/день/вечер/ночь
            morning_wind = weather_data['forecasts'][1]['parts']['morning']['wind_speed']
            day_wind = weather_data['forecasts'][1]['parts']['day']['wind_speed']
            evening_wind = weather_data['forecasts'][1]['parts']['evening']['wind_speed']
            night_wind = weather_data['forecasts'][1]['parts']['night']['wind_speed']
            return [morning_temperature, day_temperature, evening_temperature, night_temperature, morning_wind, day_wind, evening_wind, night_wind, name_place]
        except:
            return False
