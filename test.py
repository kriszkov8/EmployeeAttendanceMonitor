import os
import time
import shutil
import datetime
import mysql.connector
import csv 
import requests
import threading 
import json

class mysqlconn:
    __host="localhost"
    __user="root"
    __password="qwerty123"
    __database="employeeattendacemonitor"

    def __init__(self):
        self.database=mysql.connector.connect(
            host=self.__host,
            user=self.__user,
            password=self.__password,
            database=self.__database,
            auth_plugin='mysql_native_password'
        )
        self.cursor=self.database.cursor()
    
    def selectQuery(self,query):
        self.cursor.execute(query)
        returnable=self.cursor.fetchall()
        return returnable
    
    def truncateAllTables(self):
        self.cursor.execute('TRUNCATE PERSOANE')
        self.cursor.execute('TRUNCATE ACCES')


filesPath=r'C:/Users/Krisztian/Desktop/Tema/'
mydb=mysqlconn()

def compare(persJsonObj,persTupple):
    ok=True
    if(persJsonObj['Nume']!=persTupple[1]):
        ok=False
    if(persJsonObj['Prenume']!=persTupple[2]):
        ok=False
    if(persJsonObj['Companie']!=persTupple[3]):
        ok=False
    if(persJsonObj['IdManager']!=persTupple[4]):
        ok=False
    if(persJsonObj['Email']!=persTupple[5]):
        ok=False
    return ok

def run_test_one():
    testPassed=0
    os.system(f'python main.py 1 "{filesPath}"')
    time.sleep(1)

    shutil.copyfile(filesPath+'input_files/Poarta1.txt',filesPath+'intrari/Poarta1.txt')
    time.sleep(5)

    if 'Poarta1.txt' not in os.listdir(filesPath+'intrari'):
        print("PASSED Test 1.1")
        testPassed+=1
    else:
        print("FAILED Test 1.1")

    if f'Poarta1{datetime.date.today()}.txt' in os.listdir(filesPath+'backup_intrari'):
        testPassed+=1
        print("PASSED Test 1.2")
    else:
        print("FAILED Test 1.2")

    shutil.copyfile(filesPath+'input_files/Poarta2.csv',filesPath+'intrari\Poarta2.csv')
    time.sleep(5)

    if 'Poarta2.csv' not in os.listdir(filesPath+'intrari'):
        testPassed+=1
        print("PASSED Test 1.3")
    else:
        print("FAILED Test 1.3")

    if f'Poarta2{datetime.date.today()}.csv' in os.listdir(filesPath+'backup_intrari'):
        testPassed+=1
        print("PASSED Test 1.4")
    else:
        print("FAILED Test 1.4")
    
    dbResults=mydb.selectQuery('select * from acces')
    ok=True
    with open(filesPath+'input_files/Poarta1.txt','r') as txtFile:
        txt=txtFile.readlines()
        lenOfTxt=len(txt)
        try:
            for i,line in enumerate(txt):
                if(dbResults[i][2].strftime('%Y-%m-%dT%H:%M:%S')!=line.split(',')[1][:-5]):
                    ok=False

        except IndexError:
            print('Nu a inserat corect in baza (txt)!')

    with open(filesPath+'input_files/Poarta2.csv','r') as csvFile:
        continut=csv.reader(csvFile)
        next(continut)
        try:
            for i,line in enumerate(continut):
                if(dbResults[lenOfTxt+i][2].strftime('%Y-%m-%dT%H:%M:%S')!=line[1][:-5]):
                    ok=False
        except IndexError:
            print('Nu a inserat corect in baza (csv)')
    if ok==True:
        testPassed+=1
        print("PASSED Test 1.5")
    else:
        print("FAILED Test 1.5")

    return testPassed

def start_server():
    os.system(f'python "{filesPath}main.py" 2')
def send_request():
    with open(filesPath+'input_files/utilizatori.json','r') as jsonFile:
        data=json.load(jsonFile)
        time.sleep(5)
        for person in data:
            print(person)
            response=requests.post('5000/utilizator',json=person)
            if response.status_code!=200:
                print("Eroare la inregistrare utilizator!")
    
        utilizatori=mydb.selectQuery("SELECT * FROM persoane")
        ok=True
        for poz in range(len(data)):
            if(compare(data[poz],utilizatori[poz])==False):
                ok=False
                break
        if(ok):
            print('Test 2.1 passed!')
        else:
            print('Test 2.2 failed!')
        

def run_test_two():
    t1=threading.Thread(target=start_server)
    t2=threading.Thread(target=send_request)
    t1.start()
    t2.start()



#run_test_two()

# run_test_one()
# mydb.truncateAllTables()