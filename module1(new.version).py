
import csv
import datetime
import random
import time



# Functie om het tijdstip van het bericht op te slaan
def get_timestamp():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# Functie om een willekeurig station te kiezen uit de lijst met stations
def get_random_station():
    # Open het bestand met stations in read mode
    with open("stations.txt", "r") as file:
        all_text = file.read()
        # Split de stations op de newline-karakters en kies een willekeurig station
        stations = all_text.split('\n')
        return random.choice(stations)

# Functie om de naam van de reiziger op te vragen
def get_user_name():
    # Vraag de reiziger of hij anoniem wil zijn
    is_anonymous = input("Wilt u anoniem zijn? (ja of nee): ")

    # Als de reiziger anoniem wil zijn, retourneer de waarde "anonim"
    if is_anonymous.lower() == "ja":
        return "anoniem"
    # Als de reiziger niet anoniem wil zijn, vraag om zijn naam en retourneer deze
    else:
        name = str(input("Voer uw naam in: "))
        return name

# Functie om het bericht van de reiziger op te vragen
def get_message():
    # Vraag om het bericht van de reiziger
    message = str(input("Voer uw bericht in: "))

    # Controleer of het bericht de juiste lengte heeft
    while True:
        # Als het bericht langer is dan 140 karakters, vraag de reiziger om het te verkorten
        if len(message) > 140:
            print("Uw bericht is te lang, probeer het te verkorten (max. 140 karakters)")
            message = input("Voer uw bericht in: ")
        # Als het bericht korter is dan 2 karakters, vraag de reiziger om het te verlengen
        elif len(message) < 2:
            print("Uw bericht is te kort, probeer het te verlengen (min. 2 karakters)")
            message = input("Voer uw bericht in: ")
        # Als het bericht de juiste lengte heeft, retourneer het
        else:
            return message


while True:
    time.sleep(3)
    # Haal een willekeurig station op
    station = get_random_station()

    # Haal de naam van de reiziger op
    name = get_user_name()

    # Haal het bericht van de reiziger op
    message = get_message()
    times= get_timestamp()

    # Voeg de waarden van timestamp, station, name en message toe aan de lijst data
    data = [times, station, name, message]

    # Open het bestand "berichten.csv" in 'append' mode
    with open('berichten.csv', "a", newline='\n') as file:
        # Maak een CSV writer object
        writer = csv.writer(file, delimiter=',')

        # Schrijf de lijst van gegevens naar het bestand
        writer.writerow(data)

    print("Bedankt voor uw bericht!")