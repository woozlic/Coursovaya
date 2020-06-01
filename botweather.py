import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_bot
import requests
import random
import pymysql.cursors

#подключение к нашей бд
conn = pymysql.connect(host='woozlic.mysql.pythonanywhere-services.com',
                                 user='woozlic',
                                 password='пароль',
                                 db='woozlic$default',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
"""query = "CREATE TABLE users_places(\
user_id INT NOT NULL,\
user_place VARCHAR(100) NOT NULL,\
user_flag_change_place INT,\
PRIMARY KEY ( user_id ));"""

def write_msg(user_id, message, keyb = open("keyboard.json", "r", encoding="UTF-8").read()):
    vk.method("messages.send", {"user_id":user_id, "message":message, "keyboard":keyb, "random_id":random.randint(1,6400000)})

my_token="токен"
vk = vk_api.VkApi(token=my_token) #авторизация
place = "Москва"
now_place = "Москва"
message_commands = 'Доступные команды:\nСейчас, Сегодня, Завтра, Местоположение, Погода *название города*'
longpoll = VkLongPoll(vk,mode=234)
flag_change_place = 0 #0 - нету местоположения, 1 - установить в следующем сообщении, 2 - установлено
check_user = 0

for event in longpoll.listen(): #основной цикл
    if event.type == VkEventType.MESSAGE_NEW: #если пришло новое сообщение
        if event.to_me and event.text: #если оно имеет метку для бота
            """a = "select * from users_places"
            with conn.cursor() as cursor:
                cursor.execute(a)
                for i in cursor:
                    print(i, "-")"""
            request = event.text #сообщение от пользователя
            request = request.lower() #преобразовать сообщение к нижнему регистру
            user_id = event.user_id
            select_user_flag = "SELECT * FROM users_places WHERE user_id = {};".format(user_id)
            put_user = "INSERT INTO users_places(user_id, user_flag_change_place) VALUES({},{});".format(user_id, 0)
            with conn.cursor() as cursor:
                cursor.execute(select_user_flag)
                ans = cursor.fetchone()
                if ans:
                    flag_change_place = ans['user_flag_change_place']
                    place = ans['user_place']
                    #print(ans)
                else:
                    with conn.cursor() as cursor:
                        cursor.execute(put_user)
            #print(place, check_user, flag_change_place)
            if request == "привет":
                username = vk.method("users.get", {"user_id": user_id})[0]["first_name"]
                message = "Привет, "+str(username) + "!\n" + message_commands
                write_msg(event.user_id, message)
            elif request == "местоположение":
                write_msg(event.user_id, "Напиши название своего города\n(Пожалуйста, пишите названия без ошибок)", open("emptykeyboard.json", "r", encoding="UTF-8").read())
                #сообщение о местоположении
                update_flag = "update users_places set user_flag_change_place = 1 where user_id = {}".format(user_id)
                with conn.cursor() as cursor:
                    cursor.execute(update_flag)
                #else:
                 #   insert_flag = "INSERT INTO users_places(user_id, user_flag_change_place) VALUES({},{});".format(user_id, 1)
                  #  with conn.cursor() as cursor:
                   #     cursor.execute(insert_flag)
                #flag_change_place = 1
                #сообщение о местоположении
            elif request.split()[0] == "погода":
                if(len(request.split())>1): #погода *название города*
                    now_place = request.split()[1:]
                    now_place = " ".join(now_place)
                    weather_request = vk_bot.get_weather(now_place)
                    if(weather_request):
                        geo_lat, geo_lng, temperature, now_place = weather_request
                        message = "Сейчас погода в " + str(now_place) + " " + str(temperature) + " градусов"
                        write_msg(event.user_id, message)
                    else:
                        message = "Не удалось определить местоположение, попробуйте еще раз"
                        write_msg(event.user_id, message)
                else:
                    message = 'Пожалуйста, напишите "погода *название города*"'
                    write_msg(event.user_id, message)
            elif request == "сейчас":
                if flag_change_place == 2:
                    weather_request = vk_bot.get_weather(place)
                    if(weather_request):
                        geo_lat, geo_lng, temperature, place = weather_request
                        message = "Сейчас погода в " + str(place) + " " + str(temperature) + " градусов"
                        write_msg(event.user_id, message)
                    else:
                        message = "Не удалось определить местоположение, попробуйте ввести другое"
                        write_msg(event.user_id, message)
                else:
                    message = 'Пожалуйста, напишите "местоположение" и выберите свое местоположение или отправьте свою геолокацию с помощью кнопки'
                    write_msg(event.user_id, message)
            elif request == "сегодня":
                if flag_change_place == 2:
                    weather_today_request = vk_bot.get_weather_today(place)
                    if(weather_today_request):
                        morning_temperature, day_temperature, evening_temperature, night_temperature, morning_wind, day_wind, evening_wind, night_wind, place = \
                                             weather_today_request
                        message = "Погода на сегодня в "+str(place)+":\n\nУтром: от "+str(morning_temperature[0])+" до "+str(morning_temperature[1])+" градусов. Ветер: "+str(morning_wind)+" м/c"+\
                                  "\nДнем: от "+str(day_temperature[0])+" до "+str(day_temperature[1])+" градусов. Ветер: "+str(day_wind)+" м/c"+\
                                  "\nВечером: от "+str(evening_temperature[0])+" до "+str(evening_temperature[1])+" градусов. Ветер: "+str(evening_wind)+" м/c"+\
                                  "\nНочью: от "+str(night_temperature[0])+" до "+str(night_temperature[1])+" градусов. Ветер: "+str(night_wind)+" м/c"
                        write_msg(event.user_id, message)
                    else:
                        message = "Не удалось определить местоположение, попробуйте ввести другоe"
                        write_msg(event.user_id, message)
                else:
                    message = 'Пожалуйста, напишите "местоположение" и выберите свое местоположение или отправьте свою геолокацию с помощью кнопки'
                    write_msg(event.user_id, message)
            elif request == "завтра":
                if flag_change_place == 2:
                    weather_tommorow_request = vk_bot.get_weather_tommorow(place)
                    if(weather_tommorow_request):
                        tommorow_morning_temperature, tommorow_day_temperature, tommorow_evening_temperature, tommorow_night_temperature, tommorow_morning_wind, tommorow_day_wind, tommorow_evening_wind, tommorow_night_wind, place = \
                                             weather_tommorow_request
                        message = "Погода на завтра в "+str(place)+":\n\nУтром: от "+str(tommorow_morning_temperature[0])+" до "+str(tommorow_morning_temperature[1])+" градусов. Ветер: "+str(tommorow_morning_wind)+" м/c"+\
                                  "\nДнем: от "+str(tommorow_day_temperature[0])+" до "+str(tommorow_day_temperature[1])+" градусов. Ветер: "+str(tommorow_day_wind)+" м/c"+\
                                  "\nВечером: от "+str(tommorow_evening_temperature[0])+" до "+str(tommorow_evening_temperature[1])+" градусов. Ветер: "+str(tommorow_evening_wind)+" м/c"+\
                                  "\nНочью: от "+str(tommorow_night_temperature[0])+" до "+str(tommorow_night_temperature[1])+" градусов. Ветер: "+str(tommorow_night_wind)+" м/c"
                        write_msg(event.user_id, message)
                    else:
                        message = "Не удалось определить местоположение, попробуйте ввести другоe"
                        write_msg(event.user_id, message)
                else:
                    message = 'Пожалуйста, напишите "местоположение" и выберите свое местоположение'
                    write_msg(event.user_id, message)
            elif flag_change_place == 1: #установка местоположения
                place = request
                weather_request = vk_bot.get_weather(place)
                if(weather_request):
                    geo_lat, geo_lng, temperature, place = weather_request
                    message = "Местоположение " + str(place) + " установлено!\n"+ "Сейчас погода в " + str(place) + " - " + str(temperature) + " градусов"
                    write_msg(event.user_id, message)

                    update_flag = "update users_places set user_flag_change_place = 2 where user_id = {};".format(user_id)
                    with conn.cursor() as cursor:
                        cursor.execute(update_flag)
                    update_place = "update users_places set user_place = '{}' where user_id = {};".format(place, user_id)
                    with conn.cursor() as cursor:
                        cursor.execute(update_place)
                    #flag_change_place = 2
                else:
                    message = "Не удалось определить местоположение, попробуйте выбрать другое.\n"+ message_commands
                    write_msg(event.user_id, message)
            else:
                write_msg(event.user_id, message_commands)
connection.close()
