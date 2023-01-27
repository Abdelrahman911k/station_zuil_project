import json
from tkinter import *
from tkinter import messagebox
import psycopg2
import requests
from PIL import ImageTk
from PIL import Image

#Deze code creëert een Tkinter GUI-venster met de titel "NS" en een icon
def display_welcome():
#Vervolgens wordt de functie "display_welcome" aangeroepen die een label maakt met de tekst "Welcome to NS" in font "Olive Village" grootte 30 en een achtergrondkleur van "gold" en voegt dit toe aan de bovenkant van het venster.
 text = Label(window, text="Welcome to NS", font=("Olive Village", 30), bg='gold')
 text.pack(side=TOP)
window = Tk()



# Vervolgens wordt een afbeeldingsbestand met de naam "NS.png" geopend en geconverteerd naar een PhotoImage-object dat vervolgens aan een label wordt toegevoegd en aan het venster wordt toegevoegd
image = Image.open("NS.png")

# Converteer de afbeelding naar een PhotoImage-object
photo = ImageTk.PhotoImage(image)

# Maak een label en voeg de afbeelding eraan toe
label = Label(window, image=photo,width=450, height=290)
label.pack()



# dat is voor de window title
window.title("NS")
window.iconbitmap("Nederlandse-spoorwegen-NS-logo-.ico")
window.config(bg="gold")
#dan roep ik de functie aan
display_welcome()

#Deze code definieert drie functies: get_facilities, retrieve_facilities en hide_facilities.
def get_facilities():
    #De functie get_facilities wordt aangeroepen wanneer een gebruiker een stationsnaam invoert in een Tkinter-invoerwidget en op een knop klikt.
    # De functie controleert eerst of de gebruiker een geldige stationsnaam heeft ingevoerd, zo niet, dan wordt "Voer een geldige stationsnaam in" afgedrukt.
    # Als een geldige stationsnaam wordt ingevoerd, wordt de functie retrieve_facilities aangeroepen met de ingevoerde stationsnaam.
    station = station_entry.get()
    if station is None or station == "":
        print("Please enter a valid station name")
        return
    station = station.title()
    retrieve_facilities(station)

#de functie retrieve_facilities wordt gebruikt om verbinding te maken met een PostgreSQL-database,
def retrieve_facilities(station):
    conn = psycopg2.connect(
        database="moderation_system",
        user="postgres",
        password="Abdel2002@",
        host="localhost",
        port=54321
    )
    cursor = conn.cursor()

    # deze maakt verbinding met de database met behulp van de psycopg2-bibliotheek en haalt de faciliteiteninformatie op voor het specifieke station (ov_bike, lift, toilet, park_and_ride) uit de station_info-tabel waar de station_city gelijk is aan de ingevoerde station naam.
    cursor.execute("SELECT ov_bike, elevator, toilet, park_and_ride FROM station_info WHERE station_city = %s", (station,))
    facilities = cursor.fetchone()
    #Vervolgens maakt het een Tkinter-label widget en voegt de opgehaalde facilitaire informatie eraan toe en plaatst het op een specifieke locatie in het GUI-venster.
    if facilities:
        facility_label = Label(window,
                               text=f" ov_bike :{facilities[0]} \n  elevator :{facilities[1]}  \n  park and ride :{facilities[3]}  \n   toilet :{facilities[2]}")
        facility_label.place(x=170, y=640, width=150, height=100)
        # Het label verdwijnt ook na 3 seconden door de functie hide_facilities aan te roepen en het label door te geven als een argument dat vervolgens wordt doorgegeven aan de methode place_forget.
        facility_label.after(3000, lambda: hide_facilities(facility_label))
        #anders laat aan de gebruiker dat hij iets fout heeft gedaan
    else:
        messagebox.showerror("Error", f" ⚠️ No information available for {station} station.\n\n We have only information for these stations: \n\n Arnhem\n Almere\n Amersfoort\n Almelo\n Alkmaar\n Apeldoorn\n Assen \n Amsterdam \n Boxtel \n Breda \n Dordrecht \n Delft \n Deventer\n Enschede\n Gouda \n Groningen \n Den Haag\n Hengelo\n Haarlem\n Helmond \n Hoorn\n Heerlen \n Den Bosch\n Hilversum \n Leiden \n Lelystad\n Leeuwarden \n Maastricht \n Nijmegen \n Oss \n Roermond \n Roosendaal \n Sittard \n Tilburg \n Utrecht \nVenlo \n Vlissingen \n Zaandam \n Zwolle \n Zutphen")
# Deze functie wordt gebruikt om het label uit het GUI-venster te verwijderen door de methode place_forget op het doorgegeven label aan te roepen.
def hide_facilities(facility_label):
    #methode place_forget vertelt Tkinter om de widget van het scherm te verwijderen en de raster- en pakketinstellingen te vergeten, waardoor het label effectief voor de gebruiker wordt verborgen.
        facility_label.place_forget()

#de functie remove_review wordt gebruikt om een review uit de GUI te verwijderen door het bijbehorende label te vernietigen en het uit de review_labels-lijst te verwijderen.
review_labels = []
def remove_review(index):
    review_labels[index].destroy()
    del review_labels[index]

#Deze code maakt een knop met het label "Beoordelingen ophalen" die, wanneer erop wordt geklikt, de laatste 5 beoordelingen uit een PostgreSQL-database ophaalt en deze in labels in het venster weergeeft.
def get_reviews():
        # Connect met de Postgres database
        conn = psycopg2.connect(
            database="moderation_system",
            user="postgres",
            password="Abdel2002@",
            host="localhost",
            port=54321
        )

        cursor = conn.cursor()

        # # Haal de laatste 5 beoordelingen op volgorde van datum op
        cursor.execute("SELECT name, message, review_date_time, station FROM message ORDER BY review_date_time DESC LIMIT 5")
        reviews =  cursor.fetchall()
        #als er geen reviews zijn dan print....
        if len(reviews)==0:
            messagebox.showerror("no reviews to display")
            #anders
        else:
            # # Maak voor elke beoordeling een label
            for i, review in enumerate(reviews):
                name = review[0]
                message = review[1]
                date = review[2]
                station = review[3]
                #hiet is de form how zal het er uit zien op het scherm van het station
                review_label = Label(window, text=f"{name} - {date} - {station} : {message}",bg="gold")
                review_label.pack(ipady=10,ipadx=25,expand=YES)
                # Elk label is ook gebonden aan de functie "remove_review", zodat het, wanneer erop wordt geklikt, uit het venster en uit de lijst met beoordelings labels wordt verwijderd
                review_label.bind("<Button-1>", lambda event, index=i: remove_review(index))
                review_labels.append(review_label)
        ## Sluit de cursor en verbinding
        cursor.close()
        conn.close()
        # de button van de reviews
get_reviews_button = Button(window, text="Get reviews", command=get_reviews)
get_reviews_button.pack(ipady=25,ipadx=10,expand=YES)

def get_weather(city):
    if city is None:
        print("Invalid station name")
        return

    #deze functie een verzoek doet aan de OpenWeatherMap API om de weersvoorspelling voor een specifieke stad te krijgen
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=a40edb954201ec660390df5d9be14a4c"
    try:
        response = requests.get(url)
        data = json.loads(response.text)
        if "cod" in data and data["cod"] == "400":
            print(f"{city} not found!")
            return
        #Vervolgens ontleedt het de responsgegevens om de temperatuur, windsnelheid, breedtegraad, lengtegraad en beschrijving van het weer te extraheren.
        temperature = int(data['main']['temp'] - 273)
        wind_speed = data['wind']['speed']

        latitude = data['coord']['lat']
        longitude = data['coord']['lon']

        description = data['weather'][0]['description']

        # Het maakt een label aan om deze informatie in de GUI weer te geven en gebruikt
        weather_label = Label(window,
                              text='Temperature : {} °C \n Wind Speed : {} m/s\n Latitude : {}\n Longitude : {}\n Description : {}'.format(
                                  temperature, wind_speed, latitude, longitude, description))
        weather_label.place(x=462 - -1100, y=650, width=150, height=100)
        #De functie "hide_weather" is een geneste functie binnen de functie "get_weather". Het wordt gebruikt om het weather_label na 5 seconden uit de GUI te verwijderen
        def hide_weather():
            weather_label.after(1000, weather_label.place_forget())
# Het wordt gebruikt om het weather_label na 5 seconden uit de GUI te verwijderen.
        # De functie gebruikt de "na"-methode van de tkinter Label-widget om het verwijderen van het label na 5 seconden te plannen.
        # De methode "place_forget" wordt vervolgens aangeroepen op het weather_label om het uit de GUI te verwijderen.
        weather_label.after(5000, hide_weather)
# als er iets fout is dan laat deze bericht aan de gebruiker zien
    except Exception as e:
        messagebox.showerror(f"check if the city exists or if you made a spelling mistake: {e}")

# Maak een invoer voor de stationsnaam
weather_entry = Entry(window)
weather_entry.place(x=462 - -1100, y=600, width=150, height=20)
City_label = Label(window, text="Enter City name:", bg="#150578",fg="white")
City_label.place(x=462 - -1100, y=580, width=150, height=20)

# Maak de get_weather-knop
get_weather_button = Button(window, text="Get Weather", command=lambda: get_weather(weather_entry.get()))
get_weather_button.place(x=462 - -1100, y=462, width=150, height=50)



# # Maak een label en een vermelding voor de gebruiker om de stationsnaam in te voeren
station_label = Label(window, text="Enter station name:", bg="#150578",fg="white")
station_label.place(x=170,y=580,width=150, height=20)

station_entry = Entry(window)
station_entry.place(x=170,y=600,width=150, height=20)

# Maak een knop om de facilitaire informatie op te halen
get_facilities_button = Button(window, text="Get facilities", command=get_facilities)
get_facilities_button.place(x=170,y=469,width=150, height=50)
# show it
window.mainloop()



