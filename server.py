from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from constants import HOST, DATABASE, USER, PASSWORD
from models import User,Access

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = HOST
app.config['MYSQL_DATABASE_USER'] = USER
app.config['MYSQL_DATABASE_PASSWORD'] = PASSWORD
app.config['MYSQL_DATABASE_DB'] = DATABASE

def connect_to_database():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            passwd=PASSWORD,
            database=DATABASE
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.json
    new_user = User(nume=data['Nume'], prenume=data['Prenume'], companie=data['Companie'], IdManager=data['IdManager'])
    
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "INSERT INTO persoane (Nume, Prenume, Companie, IdManager) VALUES (%s, %s, %s, %s)"
    values = (new_user.nume, new_user.prenume, new_user.companie, new_user.IdManager)
    
    try:
        cursor.execute(query, values)
        connection.commit()
        return jsonify({"message": "User registered successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/access_log', methods=['POST'])
def access_log():
    data = request.json
    access_entry = Access(ID_Persoana=data['ID_Persoana'], Data=data['Data'], sens=data['Sens'], Poarta=data['Poarta'])
    insert_access_log(access_entry)
    return jsonify({"message": "Access log saved successfully"}), 200

def insert_access_log(access_entry):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "INSERT INTO acces (Id_Persoana, Data, Sens, Poarta) VALUES (%s, %s, %s, %s)"
    values = (access_entry.id, access_entry.ID_Persoana, access_entry.Data, access_entry.Sens, access_entry.Poarta)
    
    try:
        cursor.execute(query, values)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()

