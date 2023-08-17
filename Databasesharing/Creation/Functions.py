import pickle
import mysql.connector as sql
import os

Password = input('Password:')

Hold = sql.connect(
    host = 'localhost',
    user = 'root',
    password = Password
)
cur = Hold.cursor()

def showdatabase():
    cur.execute('show databases')
    bases = cur.fetchall()
    for b in bases:
        print(b[0])
    global database
    database = input('Database:')
    global data
    data = {database:{}}
    cur.execute('use '+ database)
    showtables()

def showtables():
    cur.execute('show tables')
    tables = cur.fetchall()
    for b in tables:
        print(b[0])

def addtable(table):
    cur.execute('describe '+ table)
    struct = cur.fetchall()
    cur.execute('select * from ' + table)
    records = cur.fetchall()
    data[database][table] = (struct,records)

def removetable(table):    
    del data[database][table]

def all():
    cur.execute('show tables')
    tables = cur.fetchall()
    for table in tables:
        addtable(table[0])

def save(filename):
    filename +='.dat'
    with open('.\\Send\\' + filename,'wb')as file:
        pickle.dump(data,file)

def tab():
    for table in data[database].keys():
        print(table)

