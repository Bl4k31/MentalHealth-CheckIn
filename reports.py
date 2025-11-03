from rich import print
import json
import psycopg2
from psycopg2 import OperationalError
import questionary
import matplotlib.pyplot as plt
import datetime
from time import sleep
database_ip_address = "127.0.0.1"
database_port = "5433"
database_name = "healthrecords"
database_user = "postgres"
database_password = ""
time_units=['hours', 'days', 'weeks', 'months', 'years']
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
def create_plot(xaxis, depression_scores, anxiety_scores, stress_scores):
    plt.figure(1)
    plt.plot(xaxis, depression_scores, label="Depression Scores")
    for x_val, y_val in zip(xaxis, depression_scores):
        plt.text(x_val, y_val, f"{y_val}", fontsize=9, ha='right', va='bottom')
    plt.plot(xaxis, anxiety_scores, label="Anxiety Scores")
    for x_val, y_val in zip(xaxis, anxiety_scores):
        plt.text(x_val, y_val, f"{y_val}", fontsize=9, ha='right', va='bottom')
    plt.plot(xaxis, stress_scores, label="Stress Scores")
    for x_val, y_val in zip(xaxis, stress_scores):
        plt.text(x_val, y_val, f"{y_val}", fontsize=9, ha='right', va='bottom')
    plt.ylim(0, 21)
    plt.title("Mental Health Scores Over Time")
    plt.xlabel("Time; Dropped off by")
    plt.ylabel("Scores")
    plt.legend()
    plt.show(block=True)
    plt.pause(0.01)  # pause to allow the plot to be updated
while True:
    time_unit = None
    time_interval = None
    print("[bold magenta]Fetch Records from Database[/bold magenta]")
    time_unit = questionary.select("Select the time interval to fetch records from:",choices=time_units).ask()
    time_interval = questionary.text("Enter the number of {}:".format(time_unit)).ask()
    time =f"{str(time_interval)} {str(time_unit)}"
    connection = create_connection(database_name, database_user, database_password, database_ip_address, database_port)
    if connection:
        # Example of creating a cursor (used to execute SQL commands)
            cursor = connection.cursor()
            sql = """SELECT * FROM main
                    WHERE date >= NOW() - INTERVAL %s;"""
            cursor.execute(sql, (time,))
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            print(rows)
    main_dates=[row[1].strftime("%d/%m/%Y\n%H:%M:%S") for row in rows]
    main_depression_scores=[row[3] for row in rows]
    main_anxiety_scores=[row[4] for row in rows]
    main_stress_scores=[row[5] for row in rows]
    main_parents=[row[6] for row in rows]
    print(main_dates)
    print(f"Depression Scores: {main_depression_scores}")
    print(f"Anxiety Scores: {main_anxiety_scores}")
    print(f"Stress Scores: {main_stress_scores}")
    print(f"Parents on weekend prior: {main_parents}")
    print("Connection closed")       
    main_xaxis=[f"{date}\n{parent}" for date, parent in zip(main_dates, main_parents)]
    create_plot(main_xaxis, main_depression_scores, main_anxiety_scores, main_stress_scores)
    if questionary.confirm("New query?").ask():
        continue
    else:
        break