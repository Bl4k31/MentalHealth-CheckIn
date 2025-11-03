from rich import print
import json
import psycopg2
from psycopg2 import OperationalError
import questionary
database_ip_address = "127.0.0.1"
database_port = "5433"
database_name = "healthrecords"
database_user = "postgres"
database_password = ""
test = False
def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
    except OperationalError as e:
            print(f"The error '{e}' occurred")
    return connection
while True:
    default_entry_json={
        1:{"text":"I found it hard to wind down", "category":"Stress", "score":0},
        2:{"text":"I was aware of dryness of my mouth", "category":"Anxiety", "score":0},
        3:{"text":"I couldn't seem to experience any positive feeling at all", "category":"Depression", "score":0},
        4:{"text":"I experienced breathing difficulty (e.g. excessively rapid breathing, breathlessness in the absence of physical exertion)", "category":"Anxiety", "score":0},
        5:{"text":"I found it difficult to work up the initiative to do things", "category":"Depression", "score":0},
        6:{"text":"I tended to over-react to situations", "category":"Stress", "score":0},
        7:{"text":"I experienced trembling (e.g. in the hands)", "category":"Anxiety", "score":0},
        8:{"text":"I felt that I was using a lot of nervous energy", "category":"Stress", "score":0},
        9:{"text":"I was worried about situations in which I might panic and make a fool of myself", "category":"Anxiety", "score":0},
        10:{"text":"I felt that I had nothing to look forward to", "category":"Depression", "score":0},
        11:{"text":"I found myself getting agitated", "category":"Stress", "score":0},
        12:{"text":"I found it difficult to relax", "category":"Stress", "score":0},
        13:{"text":"I felt down-hearted and blue", "category":"Depression", "score":0},
        14:{"text":"I was intolerant of anything that kept me from getting on with what I was doing", "category":"Stress", "score":0},
        15:{"text":"I felt I was close to panic", "category":"Anxiety", "score":0},
        16:{"text":"I was unable to become enthusiastic about anything", "category":"Depression", "score":0},
        17:{"text":"I felt I wasn't worth much as a person", "category":"Depression", "score":0},
        18:{"text":"I felt that I was rather touchy", "category":"Stress", "score":0},
        19:{"text":"I was aware of the action of my heart in the absence of physical exertion (e.g., sense of heart rate increase, heart missing a beat)", "category":"Anxiety", "score":0},
        20:{"text":"I felt scared without any good reason", "category":"Anxiety", "score":0},
        21:{"text":"I felt that life was meaningless", "category":"Depression", "score":0}
    }
    depression_score=0
    anxiety_score=0
    stress_score=0
    Scores=[0, 1, 2, 3]
    for key in default_entry_json:
        print(f"[blue][underline]{default_entry_json[key]['text']}[/underline][/blue]")
        while True:
            try:
                user_input = int(input("Enter your score (0-3): "))
                if user_input in Scores:
                    default_entry_json[key]['score'] = user_input
                    break
                else:
                    print("Invalid input. Please enter a number between 0 and 3.")
            except ValueError:
                print("Invalid input. Please enter a valid integer between 0 and 3.")

    print("Scores:")
    for key in default_entry_json:
        if default_entry_json[key]['category'] == "Depression":
            depression_score += default_entry_json[key]['score']
        elif default_entry_json[key]['category'] == "Anxiety":
            anxiety_score += default_entry_json[key]['score']
        elif default_entry_json[key]['category'] == "Stress":
            stress_score += default_entry_json[key]['score']

    print(f"Depression Score: {depression_score}")
    print(f"Anxiety Score: {anxiety_score}")
    print(f"Stress Score: {stress_score}")
    field_data = json.dumps(default_entry_json)
    parents=["Mum","Dad"]
    parent = questionary.select("What parent dropped you off at school today?",choices=parents).ask()

    if questionary.confirm("Do you believe the data you entered is accurate to the best of your knowledge?").ask():
        if test:
            break
        else:
            confirmed_details_accurate=True
            connection = create_connection(database_name, database_user, database_password, database_ip_address, database_port)
            if connection:
                # Example of creating a cursor (used to execute SQL commands)
                    cursor = connection.cursor()
                    sql = """INSERT INTO main (field_data, depression_score, anxiety_score, stress_score, last_parent, comfirmed_details_accurate)
                                VALUES (%s, %s, %s, %s, %s, %s);"""
                    cursor.execute(sql, (field_data, depression_score, anxiety_score, stress_score, parent, confirmed_details_accurate))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    print("Connection closed")
            break
    else:
        print("[red][bold]Restarting form...[/bold][/red]")

