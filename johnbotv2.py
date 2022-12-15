
from tkinter import *
import os
from johnbot import *
import openpyxl
import time

def teach():
    with open('combdict.json') as json_file:
            combdict = json.load(json_file)

    jdf = pd.read_excel("word-data.xlsx")
    for col in jdf.columns:    
        jdf[col] = jdf[col].str.lower()
    jdf = jdf.rename(str.lower, axis='columns')

    e.delete(0, END)
    txt.insert(END, "\n" + f"johnBot: Okay, what word are you tryna teach me?")
    engine.say('Okay, what are you tryna teach me?')
    engine.runAndWait()
    sendb.configure(text='Send-y', command=gety) # this should change the original function of the Send button, if it doesn't find way to do so because everything else should be done.

def gety():
    global y
    y = e.get().strip(' ').lower()
    txt.insert(END, "\n" + f"You: {e.get()}")
    txt.insert(END, "\n" + f"johnBot: What the fuck is that, in 1 word?")
    engine.say('What the fuck is that, in 1 word?')
    engine.runAndWait()
    e.delete(0, END)
    sendb.configure(text='Send-x', command=getx)

def getx():
    jdf = pd.read_excel("word-data.xlsx")
    for col in jdf.columns:    
        jdf[col] = jdf[col].str.lower()
    jdf = jdf.rename(str.lower, axis='columns')

    global z
    z = e.get().strip(' ').lower()
    txt.insert(END, "\n" + f"You: {e.get()}")
    e.delete(0, END)
    if z in list(jdf.columns): # append to existing column
        with open('combdict.json') as json_file:
            combdict = json.load(json_file)
            
        if jdf[z].isnull().values.any() == True:
            jdf[z][jdf[z].loc[jdf[z].isnull()].index[0]] = y
        else:
            df = pd.Series([np.nan for x in list(jdf.columns)], index = list(jdf.columns))
            df[z] = y
            jdf = jdf.append(df,ignore_index=True)

        # Saving files 
        os.remove('word-data.xlsx')
        jdf.to_excel("word-data.xlsx", index=False)
        with open("combdict.json", "w") as outfile:
            json.dump(combdict, outfile, indent=4)    

        e.delete(0, END)
        txt.insert(END, "\n" + f"johnBot: Thanks for teaching me, now Im one step closer towards the ultimate intellect of the great Antonio")
        engine.say('Thanks for teaching me, now Im one step closer towards the ultimate intellect of the great Antonio')
        engine.runAndWait()
        sendb.config(text='Send', command=send)
    
    else: # create new column with new value
        txt.insert(END, "\n" + f"johnBot: Can you explain what {z} is in a sentence?")
        engine.say(f'Can you explain what {z} is in a sentence?')
        engine.runAndWait()
        sendb.configure(text='Send-z', command=getz)

def getz():
    with open('combdict.json') as json_file:
        combdict = json.load(json_file)
    jdf = pd.read_excel("word-data.xlsx")
    for col in jdf.columns:    
        jdf[col] = jdf[col].str.lower()
    jdf = jdf.rename(str.lower, axis='columns')

    s = e.get().strip(' ').lower()
    txt.insert(END, "\n" + f"You: {e.get()}")
    jdf[z] = np.nan
    inum = jdf[z].loc[jdf[z].isnull()].index[0]
    jdf[z][inum] = y
    combdict[z] = f'Some loser told me that {y} means {s}' # appending new response to combdict dictionary

    # Saving files 
    os.remove('word-data.xlsx')
    jdf.to_excel("word-data.xlsx", index=False)
    with open("combdict.json", "w") as outfile:
        json.dump(combdict, outfile, indent=4)    

    e.delete(0, END)
    txt.insert(END, "\n" + f"johnBot: Thanks for teaching me, now Im one step closer towards the ultimate intellect of the great Antonio")
    engine.say('Thanks for teaching me, now Im one step closer towards the ultimate intellect of the great Antonio')
    engine.runAndWait()
    sendb.configure(text='Send', command=send)

# Johnbot GUI
root = Tk()
root.title("JohnBot")
root.iconbitmap("johnboticon.ico")
BG_COLOR = "#93CAED"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

#johnbot
def johnbot2(saytence):
    with open('combdict.json') as json_file:
        combdict = json.load(json_file)

    jdf = pd.read_excel("word-data.xlsx")
    for col in jdf.columns:    
        jdf[col] = jdf[col].str.lower()
        
    jdf = jdf.rename(str.lower, axis='columns')
    
    # cleaning combination
    cc = combsent(saytence).split('-')
    combdone = ''.join(cc)
    
    try:
        return combdict[combdone]
    except:
        return "Fuck you, My IQ is way to low to understand the shit your saying"

# Send function
def send():
    txt.insert(END, "\n" + f"You: {e.get()}")
 
    user = e.get().lower()

    if user == 'can i teach you something?':
        teach()   

    elif (user == 'can you beat box?') | (user == 'can you beatbox?') | (user == 'can you beat-box?'):
        beat = "boots and cats boots and cats boots and cats Fuck you"
        txt.insert(END, "\n" + f"johnBot: {beat}")
        engine.say(beat)
        engine.runAndWait()

    else:
        txt.insert(END, "\n" + f"johnBot: {johnbot2(user)}")
        engine.say(johnbot2(user))
        engine.runAndWait()
 
    e.delete(0, END)
 
 
lable1 = Label(root, bg=BG_COLOR, fg='black', text="JohnBot", font=FONT_BOLD, pady=10, width=20, height=1).grid(row=0, column=0)
 
txt = Text(root, bg=BG_COLOR, fg='black', font=FONT, width=60)
txt.grid(row=1, column=0, columnspan=2)
 
scroll = Scrollbar(txt)
scroll.place(relheight=1, relx=0.974)
 
e = Entry(root, bg="#2C3E50", fg="#EAECEE", font=FONT, width=55)
e.grid(row=2, column=0)
 
sendb = Button(root, text="Send", font=FONT_BOLD, bg="#ABB2B9", command=send)
sendb.grid(row=2, column=1)
root.mainloop()