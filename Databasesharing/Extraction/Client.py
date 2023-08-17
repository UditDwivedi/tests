import mysql.connector as sql
import pickle

PASSWORD = input('Password:')

main = sql.connect(
    host = 'localhost',
    user = 'root',
    password = PASSWORD
)
cur = main.cursor()

def commitexecute(query):
    cur.execute(query)
    main.commit()

def checkdatabase(database):
    cur.execute('show databases')
    result = cur.fetchall()
    if (database,) not in result:
        return False
    else:
        return True

def createtable(tablename,struct):
    finalquery = 'create table ' + tablename
    types = '('
    count = 0
    for s in struct:
        Struct = []
        for S in s:
            if type(S) == bytes:
                S = S.decode()
            Struct.append(S)
                
        a,b,c,d,e,f = Struct        
        addstr = a+' '
        addstr += b+' '

        types += addstr+','
        count += 1
    finalquery += types[:-1]+')'

    commitexecute(finalquery)

def filltable(table,data):
    if len(data) > 0:
        l = len(data[0])
        query = 'insert into ' + table+ ' values('+'%s,'*l
        cur.executemany(query[:-1]+')',data)
        main.commit()

filename = input('Filename:')+'.dat'
with open('.\\Data\\'+filename,'rb') as file:
    data = pickle.load(file)

database = list(data.keys())[0]
priority = False

if not checkdatabase(database):
    commitexecute('create database ' + database)
else:
    print('If any tables of same name exist')
    print('Do you wish to overwrite tables in your database')
    if input('y/n : ') == 'y':
        priority = True

cur.execute('use ' + database)

tables = data[database]
cur.execute('show tables')
databasetables = cur.fetchall()

for table in databasetables:
    if table[0] in tables:
        if priority:
            commitexecute('drop table '+table[0])
        else:
            del tables[table[0]]

print(database)

for table in tables:
    createtable(table,tables[table][0])
    print('Created table '+table)
    filltable(table,tables[table][1])
    print('Inserted into table ' + table)




