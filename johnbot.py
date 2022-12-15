import pandas as pd
import numpy as np
import warnings
import json
warnings.filterwarnings('ignore')
import os
import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 200)

main = pd.read_excel("word-data.xlsx")
for col in main.columns:  
    main[col] = main[col].str.lower()

main = main.rename(str.lower, axis='columns')

mainum = main.rename(columns={'curious': '0','anger': '1','sad': '2','innapropriate': '3','loving': '4','nervous': '5',
                            'happy': '6','scared': '7','upset': '8','disgust': '9','badw': 'a','seduce': 'b',
                            'intro': 'c','bye': 'd','custom': "e",'question': 'q'})

def category(word):
    main = pd.read_excel("word-data.xlsx")
    for col in main.columns:  
        main[col] = main[col].str.lower()

    main = main.rename(str.lower, axis='columns')

    mainum = main.rename(columns={'curious': '0','anger': '1','sad': '2','innapropriate': '3','loving': '4','nervous': '5',
                                'happy': '6','scared': '7','upset': '8','disgust': '9','badw': 'a','seduce': 'b',
                                'intro': 'c','bye': 'd','custom': "e",'question': 'q'})

    nocate = 0
    for col in mainum.columns: # decide what dataset you use here
        if word.lower() in mainum[col].unique():
            return col
            break
        else:
            nocate += 1
            continue
        
    if nocate == len(mainum.columns):
        #print('Fuck you')
        return ''


def combsent(sentence):
    main = pd.read_excel("word-data.xlsx")
    for col in main.columns:  
        main[col] = main[col].str.lower()

    main = main.rename(str.lower, axis='columns')

    combination = ''
    punctuation = ['.','?','!']
    
    if any(substring in sentence for substring in punctuation):
        strl = list(sentence)
        punc = strl[-1]
        strl[-1] = f' {strl[-1]}'

        sentence = "".join(strl)
    
    
    slb = sentence.split(' ')
    slbb = set(slb)
    slist = list(slbb)
    
    for s in slist:
        if str(category(s)) == '':
            #combination += ''
            pass
        else:
            combination += f'{str(category(s))} '
            
    # sorting order in alphabetical order
    comblb = combination.split(' ')
    comblbb = set(comblb) # make it unique
    combl = list(comblbb)
    comba = sorted(combl)
    
    combaa = [x+'-' for x in comba if x != '']
    combf = ''.join(combaa)
    
    # If combination is higher than 2
    fixl = sorted(combf.split('-'))
    fixl.remove('')
    
    if len(fixl) > 2 or any(x in fixl for x in list(main.columns)):
        # if a word in column matches column in main dataframe
        for w in fixl:
            if w in list(main.columns):
                completecomb = w
                break
            if fixl.index(w) == (len(fixl) - 1):
                # if it doesnt and it just has more than 2 column values
                compcomb = [x+'-' for x in fixl if x != '']
                completecomb = ''.join(compcomb[0:2])
                break
            continue
        
        return completecomb
    else:
        return combf

def johnbot():
    off = 0
    with open('combdict.json') as json_file:
        combdict = json.load(json_file)

    while (off == 0):

        jdf = pd.read_excel("word-data.xlsx")
        for col in jdf.columns:    
            jdf[col] = jdf[col].str.lower()
            
        jdf = jdf.rename(str.lower, axis='columns')
        x = input('Say something:').lower()
        if x == 'can i teach you something?':
            print('Okay, what are you tryna teach me?')
            engine.say('Okay, what are you tryna teach me?')
            engine.runAndWait()
            y = input('What word are you tryna teach him?: ').strip(' ').lower()
            z = input('What the fuck is that, in 1 word?: ').strip(' ').lower()
    
            if z in list(jdf.columns): # append to existing column
                if jdf[z].isnull().values.any() == True:
                    jdf[z][jdf[z].loc[jdf[z].isnull()].index[0]] = y
                else:
                    df = pd.Series([np.nan for x in list(jdf.columns)], index = list(jdf.columns))
                    df[z] = y
                    jdf = jdf.append(df,ignore_index=True)
            
            else: # create new column with new value
                s = input(f'Can you explain what {z} is in a sentence: ').lower()
                jdf[z] = np.nan
                inum = jdf[z].loc[jdf[z].isnull()].index[0]
                jdf[z][inum] = y
                
                combdict[z] = f'Some loser told that {y} means {s}' # appending new response to combdict dictionary
            
            # Saving files 
            os.remove('word-data.xlsx')
            jdf.to_excel("word-data.xlsx", index=False)
            with open("combdict.json", "w") as outfile:
                json.dump(combdict, outfile, indent=4)    

            print('Thanks for teaching me, now Im one step closer towards the ultimate intellect of the great Antonio')
            engine.say("Thanks for teaching me, now Im one step closer towards the ultimate intellect of the great Antonio")
            engine.runAndWait()
            continue # skips rest of loop, moving back to the top
        
        # cleaning combination
        cc = combsent(x).split('-')
        combdone = ''.join(cc)
        
        try:
            print(combdict[combdone])
            engine.say(combdict[combdone])
            engine.runAndWait()
        except:
            print(combdone)
            print("Fuck you, My IQ is way to low to understand the shit your saying")
            engine.say("Fuck you, My IQ is way to low to understand the shit your saying")
            engine.runAndWait()

#johnbot()