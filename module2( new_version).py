import psycopg2
import datetime
import random

now = datetime.datetime.now()
time=(now.strftime("%Y-%m-%d  %H:%M:%S"))
print(time)

##ik heb een functie gedefinieerd genaamd "locatie" die een tekstbestand "stations.txt" opent en de inhoud van het bestand leest en een willekeurige regel toewijst aan de variabele "station".
def locatie():
    # Open the file in read mode
    with open("stations.txt", "r") as file:
        allText = file.read()
        global station
        words = list(map(str, allText.split('\n')))
        station = random.choice(words)


#De functies "moderator_id",
# "mod_naam"
# "mail" worden gebruikt om de moderator te vragen respectievelijk zijn
# ID, naam en e-mailadres in te voeren en de invoer toe te wijzen aan globale variabelen.
def moderator_id():
   global ID
   ID = input('wat is uw ID: ')
   return ID


def mod_naam():
    global naam
    naam = str(input('Vul uw naam in: '))


def mail():
 global email
 email = str(input('wat is uw email?: '))




#De functie "bericht_naar_database" neemt een ingevoerd "bericht"
def bericht_naar_database(bericht):

        # en splitst het bericht op in een lijst met waarden.
        values = bericht.split(',')

        # Vervolgens maakt het verbinding met de database en maakt het een cursor object.
        conn = psycopg2.connect(
            database="moderation_system",
            user="postgres",
            password="Abdel2002@",
            host="localhost",
            port=54321
        )

        # Maak een cursor object
        cur = conn.cursor()


        # Vervolgens voegt het een rij in de berichten tabel in met de waarden uit de lijst, evenals de huidige datum, tijd en moderator-ID
        query2 = "INSERT INTO message (date_time, name, station, message, approval_status, review_date_time, moderator_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data2 = (values[0], values[2], values[1], values[3], "goedgekeurd", time,ID )
        cur.execute(query2, data2)
        conn.commit()

        # Sluit de cursor en verbinding
        cur.close()
        conn.close()


def check_bericht():
#De functie "check_bericht" opent een bestand "berichten.csv" en leest de inhoud van het bestand.
        try:
            bestand = open('berichten.csv', 'r')
            berichten = bestand.readlines()
# Vervolgens doorloopt het de berichten
            for bericht in berichten:
                print(bericht)
                # en vraagt de moderator het bericht goed te keuren of af te wijzen
                goedkeuring = input('type ja of nee: ')
                while True:
#en roept de functie "bericht_naar_database" aan om het bericht in de database in te voegen als het is goedgekeurd
                    if goedkeuring == 'ja':
                        print('bericht goedgekeurd')
                        bericht_naar_database(bericht)
## Schrijf de bijgewerkte lijst met berichten terug naar het bestand
                        with open('berichten.csv', 'w') as file:
                            for message in berichten:
                                file.write(message)
                        break
##als de moderator het bericht heeft afgekeurd dan blijft voorlopig in het bestand en met behulp van functie remove_berichten wordt het verwijderd uit het bestand.
                    elif goedkeuring == 'nee':
                        print('bericht afgekeurd')
                        break
                        # als de moderator andere woorden heeft getypt dan het wordt niet van hem geaccepteerd en moet hij nog een keer moet ja of niet in voren.
                    else:
                        goedkeuring = input("opnieuw proberen met ja of nee :")
                        #Als de moderator niet bestaat, wordt de gebruiker gevraagd een geldig ID, naam en e-mailadres in te voeren.
        except Exception as e:
            print("Moderator does not exist:", "Please enter a valid ID / moderator naam / email ")
#In plaats van het programma vanaf het begin terug te sturen, keert het programma het automatisch terug naar de invoercel
            while True:
                moderator_id()
                mod_naam()
                mail()
 ##De try-except block wordt gebruikt om te controleren of de moderator bestaat in de database.
                try:
                    check_bericht()

###De break statement zorgt ervoor dat de loop stopt zodra een geldig ID, naam en e-mailadres zijn ingevoerd en de check_bericht functie wordt uitgevoerd.
                    break
                except Exception as e:
                    print("Moderator does not exist:", "Please enter a valid ID / moderator naam / email ")

#De functie "remove_berichten" opent het bestand "berichten.csv" en kapt de inhoud van het bestand af.
def remove_berichten():
    ## Open het bestand in schrijfmodus
    bestand = open('berichten.csv', 'w')
# Maak de inhoud van het bestand leeg
#truncate is Wanneer de methode wordt aangeroepen, worden alle gegevens in het bestand verwijderd
    bestand.truncate(0)
#sluit het bestand
    bestand.close
    # Retourneer een bericht dat aangeeft dat het bestand nu leeg is
    return ('file is leeg')

#Ten slotte roept het script de functies moderator_id,
# mod_naam,
# mail en check_bericht aan
# en verwijdert het de berichten door de functie remove_berichten aan te roepen.
moderator_id()
mod_naam()
mail()
check_bericht()
remove_berichten()








