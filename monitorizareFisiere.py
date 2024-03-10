import os
import shutil
import time
import csv
import mysql.connector
from mysql.connector import Error
from models import Access
from constants import ENTRIES_DIR, BACKUP_ENTRIES_DIR, HOST, USER, PASSWORD,DATABASE
from server import insert_access_log
from datetime import datetime


class mysqlconn:
    host=HOST
    User=USER
    password=PASSWORD
    database=DATABASE


def insert_access_log(id_user, datetime_iso, sens, id_poarta):
    mydb=mysqlconn()
    connection = mysql.connector.connect(
    host=mydb.host,
    user=mydb.User,
    passwd=mydb.password,
    database=mydb.database
    )
    cursor = connection.cursor()
    datetime_formatted = datetime_iso.replace('T', ' ').split('.')[0]
    query = "INSERT INTO Acces (Id_Persoana, Data, Sens, Poarta) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (id_user, datetime_formatted, sens, id_poarta))
    connection.commit()

def process_file(filepath, filename):
    id_poarta = filename.split('Poarta')[1].split('.')[0]
    with open(filepath, 'r') as file:
        for line in file:
            id_user, datetime_iso, sens = line.strip().rstrip(';').split(',')
            insert_access_log(id_user, datetime_iso, sens, id_poarta)

def move_to_backup(source, destination):
    shutil.move(source, destination)

def monitor_folder(directory=ENTRIES_DIR):
    while True:
        for filename in os.listdir(directory):
            if filename.startswith('Poarta') and (filename.endswith('.csv') or filename.endswith('.txt')):
                filepath = os.path.join(directory, filename)
                process_file(filepath, filename)
                backup_path = os.path.join(BACKUP_ENTRIES_DIR, filename)
                move_to_backup(filepath, backup_path)
        time.sleep(10)  # Așteaptă 10 secunde înainte de a verifica din nou

def calculate_working_hours():
        connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        cursor = connection.cursor()
        query = """
        SELECT Id_Persoana, Data, Sens FROM Acces
        WHERE DATE(Data) = CURDATE() - INTERVAL 1 DAY
        ORDER BY Id_Persoana, Data;
        """
        cursor.execute(query)
        logs = cursor.fetchall()
        
        user_hours = {}
        for user_id, datetime_str, direction in logs:

            datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%D %H:%M:%S')
                
            if (user_id) not in (user_hours):
                user_hours[user_id] = []
                
            user_hours[user_id].append((datetime_obj, direction))

        for user_id, entries in user_hours.items():
            total_hours = 0
            in_time = None
            for datetime_obj, direction in entries:
                if direction == 'in':
                    in_time = datetime_obj
                elif direction == 'out' and in_time:
                    total_hours += (datetime_obj - in_time).total_seconds() / 3600
                    in_time = None 
            print(f"User {user_id} worked {total_hours} hours.")

def underworkers(user_hours, backup_directory):
    current_date_str = datetime.now().strftime("%Y-%m-%d")
    csv_file_path = os.path.join(backup_directory, f"{current_date_str}_chiulangii.csv")
    txt_file_path = os.path.join(backup_directory, f"{current_date_str}_chiulangii.txt")
    
    underworked_users = [(user_id, info['total_hours']) for user_id, info in user_hours.items() if info['total_hours'] < 8]
    
    with open(csv_file_path, 'w', encoding='utf-8') as csv_file:
        csv_file.write("Nume,OreLucrate\n")
        for user_id, hours in underworked_users:
            csv_file.write(f"{user_id},{hours}\n")
    

    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        for user_id, hours in underworked_users:
            txt_file.write(f"{user_id},{hours}\n")
    
    print(f"Rapoarte pentru angajații cu ore insuficiente au fost scrise in {csv_file_path} si {txt_file_path}.")

