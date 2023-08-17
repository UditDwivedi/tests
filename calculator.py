from tkinter import *

root = Tk()
root.title("Calculator")

font1 = ("Roboto",16,"bold")

entry = Entry(root,width=20, font=font1, bd=5)
entry.insert(0,'')

def do_click(n,keep=True):
    cur = ''
    if keep:
        cur = entry.get()
    new = cur + n
    entry.delete(0,END)
    entry.insert(0,new)

def disable_button():
    buttons[0][3]['state'] = DISABLED
    buttons[1][3]['state'] = DISABLED
    buttons[2][3]['state'] = DISABLED
    buttons[3][3]['state'] = DISABLED
def enable_button():
    buttons[0][3]['state'] = NORMAL
    buttons[1][3]['state'] = NORMAL
    buttons[2][3]['state'] = NORMAL
    buttons[3][3]['state'] = NORMAL
    
def do_add():
    disable_button()
    do_click('+')
def do_sub():
    disable_button()
    do_click('-')
def do_multi():
    disable_button()
    do_click('x')
def do_div():
    disable_button()
    do_click('/')

def do_clear():
    enable_button()
    entry.delete(0,END)

def do_equal():
    equation = entry.get()
    enable_button()
    if '+' in equation:
        eq =  equation.split('+')
        do_click(str(int(eq[0])+int(eq[1])),False)
    elif '-' in equation:
        eq =  equation.split('-')
        do_click(str(int(eq[0])-int(eq[1])),False)
    elif 'x' in equation:
        eq =  equation.split('x')
        do_click(str(int(eq[0])*int(eq[1])),False)
    elif '/' in equation:
        eq =  equation.split('/')
        do_click(str(int(eq[0])//int(eq[1])),False)

buttons = [
    [
        Button(root, text='7',width=4, height=1, command= lambda:do_click('7')),
        Button(root, text='8',width=4, height=1, command= lambda:do_click('8')),
        Button(root, text='9',width=4, height=1, command= lambda:do_click('9')),
        Button(root, text='+',width=4, height=1, command=do_add)
    ],
    [
        Button(root, text='4',width=4, height=1, command= lambda:do_click('4')),
        Button(root, text='5',width=4, height=1, command= lambda:do_click('5')),
        Button(root, text='6',width=4, height=1, command= lambda:do_click('6')),
        Button(root, text='-',width=4, height=1, command=do_sub)
    ],
    [
        Button(root, text='1',width=4, height=1, command= lambda:do_click('1')),
        Button(root, text='2',width=4, height=1, command= lambda:do_click('2')),
        Button(root, text='3',width=4, height=1, command= lambda:do_click('3')),
        Button(root, text='x',width=4, height=1, command=do_multi)
    ],
    [
        Button(root, text='0',width=4, height=1, command= lambda:do_click('0')),
        Button(root, text='=',width=4, height=1, command=do_equal),
        Button(root, text='C',width=4, height=1, command=do_clear),
        Button(root, text='/',width=4, height=1, command=do_div)
    ]
    ]

entry.grid(row=0, column=0, columnspan=5)

for r in range(4):
    for c in range(4):
        button = buttons[r][c]
        button.configure(font=font1)
        button.grid(row=r+1, column=c)

root.mainloop()
