#Deze code definieert verschillende functies die worden gebruikt om gegevens in een database in te voegen
import psycopg2

#De functies moderator_id(), mod_naam() en mail() worden gebruikt om input van de gebruiker te verzamelen,
#die vervolgens wordt gebruikt om een nieuwe rij in te voegen in de moderator tabel van de moderation_system database.
def moderator_id():
    global ID
    ID = input('Enter your ID: ')
    return ID


def mod_naam():
    global naam
    naam = str(input('Enter your name: '))
    return naam


def mail():
    global email
    email = str(input('Enter your email: '))
    return email

#De functie insert_into_database() wordt gebruikt om verbinding te maken met de database
def insert_into_database():
    moderator_id()
    mod_naam()
    mail()
    try:
        # Connect to the database
        conn = psycopg2.connect(
            database="moderation_system",
            user="postgres",
            password="Abdel2002@",
            host="localhost",
            port=54321
        )

        #  en een cursor object te maken
        cur = conn.cursor()

        # Insert a row into the moderator table
        # en vervolgens de gegevens in de moderator tabel in te voegen met behulp van een Pgadmin-query.
        query1 = "INSERT INTO moderator (moderator_id, name, email) VALUES (%s, %s, %s)"
        data1 = (ID, naam, email)
        cur.execute(query1, data1)
        conn.commit()
#De gegevens worden vastgelegd in de database en als er een fout optreedt, worden deze afgedrukt.
        print("Data inserted successfully.")
    except psycopg2.Error as e:
        print(e)
# Ten slotte zijn de cursor en de verbinding gesloten.
    finally:
        cur.close()
        conn.close()

#en hier heb ik de functie aan geroepen
insert_into_database()
