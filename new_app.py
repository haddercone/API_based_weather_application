from tkinter import *
from key import api_key
import requests
import base64
from urllib.request import urlopen
import geocoder


def search():
    try:
        city_name = entry_field.get()
        if city_name is None:
            pass
        else:
            link = 'https://api.openweathermap.org/data/2.5/weather?'
            param = {'q': city_name, 'appid': api_key}
            data = requests.get(url=link, params=param)
            # print(data.url)
            data = data.json()

            Label(frame, text="             Weather in " + data['name']+', ' + data['sys']['country']+'            ',
                  font='Roboto 20 bold', bg='#fff').grid(row=6, pady=5, columnspan=2)

            temp = data['main']['temp'] - 273.15

            icon = data['weather'][0]['icon']
            url = 'http://openweathermap.org/img/wn/' + icon + '@2x.png'
            image_byt = urlopen(url).read()
            image_b64 = base64.encodebytes(image_byt)
            photo = PhotoImage(data=image_b64)
            # create a white canvas
            cv = Canvas(frame, bg='white')
            cv.config(width=100, height=100)
            # put the image on the canvas with
            # create_image(xpos, ypos, image, anchor)
            cv.create_image(1, 1, image=photo, anchor='nw')
            cv.grid(row=7, column=0, columnspan=2)

            Label(frame, text="                  " + data['weather'][0]['description'] + "                  ".capitalize(),bg="#fff",
                  font='Roboto 13 normal').grid(row=8, pady=5, columnspan=2)

            Label(frame, text="  %.2f°C  " % temp, bg="#fff",
                  font='Roboto 20 bold').grid(row=9, pady=5, columnspan=2)

            temp_min = data['main']['temp_min'] - 273.15
            Label(frame, text="Minimum temperature : %.2f°C " % temp_min, bg="#fff",
                  font='Roboto 13 normal').grid(row=10, column=0, ipady=5, ipadx=5)

            temp_max = data['main']['temp_max'] - 273.15
            Label(frame, text="Maximum temperature : %.2f°C " % temp_max, bg="#fff",
                  font='Roboto 13 normal').grid(row=11, column=0, ipady=5, ipadx=5)

            pressure = data['main']['pressure']*100
            Label(frame, text="   Atmospheric pressure:"+str(pressure)+" Pa   ", bg="#fff",
                  font='Roboto 13 normal').grid(row=10, column=1, ipady=5, ipadx=5)

            Label(frame, text="Humidity: "+str(data['main']['humidity'])+" %", bg="#fff",
                  font='Roboto 13 normal').grid(row=11, column=1, ipady=5, ipadx=5)

            Label(frame, text="Wind speed: "+str(data['wind']['speed'])+" m/s", bg="#fff",
                  font='Roboto 13 normal').grid(row=12, column=0, ipady=5, ipadx=5)

            Label(frame, text="Clouds "+str(data['clouds']['all'])+" %", bg="#fff",
                  font='Roboto 13 normal').grid(row=12, column=1, ipady=5, ipadx=5)

            root.mainloop()

    except KeyError:
        Label(frame, text="           Please enter correct data            ",
              font='Roboto 17 bold', bg='#fff').grid(row=6, columnspan=2)


root = Tk(className="Weather App")
root.config(background='#fff')
root.minsize(565, 210)


loc = geocoder.ip('me') # gets your current location with help of your ip address.
data = loc.geojson
# print(data)
default_city_name = data['features'][0]['properties']['city']

frame = Frame(root)
frame.config(background='#fff')
frame.pack()

label_1 = Label(frame, text="Weather App", fg="#2e2e2e", bg='#fff',
                font='Roboto 17 bold').grid(row=0, columnspan=2)

label_2 = Label(frame, text="Get weather data by city names", fg="#2e2e2e", bg='#fff',
                font='Roboto 13 normal').grid(row=2, columnspan=2)

label_3 = Label(frame, text="Enter city name ", fg="#2e2e2e", bg='#fff',
                font='Roboto 13 normal').grid(row=3, padx=5, pady=15, columnspan=2)

entry_field = Entry(frame, bd=3, bg='#dfd', fg='#2e2e2e', justify='center')
entry_field.insert(END, default_city_name)
entry_field.config(font=('Roboto', 13))
entry_field.grid(row=4, ipadx=20, ipady=5, padx=10, columnspan=2)

button = Button(frame, text='Search', font='Roboto 12 normal', command=search)
button.grid(row=5, pady=15, columnspan=2)
root.wait_visibility()
search()
root.mainloop()
