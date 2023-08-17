import Functions as f
import tabulate as t

Database = None
run = True
comm = 'change'
def help():
    Help = [['Commands','Function'],
    ['change','Change current working database'],
    ['show','Display all the tables in the database'],
    ['add','Add a table in the from the database into the file'],
    ['all','add all the tables from the database into the file'],
    ['remove','Remove a table from the file'],
    ['tab','Display all the tables in the file'],
    ['save','Save the file'],
    ['end','end the program']]
    print(t.tabulate(Help))

while run:

    if comm == 'change':       
        f.showdatabase()
    elif comm == 'end':
        break
    elif comm == 'show':
        f.showtables()
    elif comm == 'add':
        f.addtable(input('Table:'))
    elif comm == 'all':
        f.all()
    elif comm == 'remove':
        f.removetable(input('Table:'))
    elif comm == 'save':
        f.save(input('Filename:'))
    elif comm == 'tab':
        f.tab()
    elif comm == 'help':
        help()
    else:
        print('invalid command')
    

    comm = input('command:')
 