from tkinter import*
from tkinter import simpledialog
from tkinter import messagebox
import tkinter
import ast # txt - dict muunnokseen
from datetime import date, datetime
from functools import partial


# This is a demo for simple proof-of-consept purpose. Do not use in production environments or with real data!


# näytelista alussa apuna, nyt ei käytetä

#näytelista = ["vesinäyte", "ilmanäyte"]
#apu_näytelista = [] #tarkistetaan onko näyte jo tulostettu ruudulle, ei enää käyttöä


#tulokset-sanakirja helpottaa devausta, kommentoi pois ja ota tyhjä sanakirja tilalle
tulokset = {'vesinäyte': {'tulokset': {'puhtaus': '100 %', 'COD': '1,5 mmol/l'}}, 'ilmanäyte': {'tulokset': {'puhtaus': '90 %', 'COD': '5,5 mmol/l'}}, 'likavesinäyte': {'tulokset': {'puhtaus': '85 %', 'COD': '50 mmol/l'}}, 'juomavesi': {'tulokset': {'puhtaus': '35 %', 'COD': '65 mmol/l', 'Salmonella': 'Havaittu'}}, 'likavesinäyte 11.5': {'tulokset': {'puhtaus': '87 %', 'COD': '30 mmol/l'}},'likavesinäyte 16.5': {'tulokset': {'puhtaus': '92 %', 'COD': '85 mmol/l'}}}
#tulokset = {}
apu_tulokset =[]



#lokikirja
lokikirja = []  #tehdään yksinkertainen lista, jatkossa sanakirja olisi parempi
lokikirja_tiedosto = ""

näytetiedosto = ""

#kayttajan tiedot
kayttajat = ["Kalle Kallela"]
kayttaja = kayttajat[0]  #jatkossa voi lisätä eri käyttäjille omat tilit, nyt vain lokikirjan testaukseen yksi nimi
rooli = "Kemisti" #Jatkossa voisi olla eri rooleja eri oikeuksin, esim. tulokset ja näytteet lisää eri henkilö -> väärinkäytön estäminen

#ikkunan koko ja muotoilu

root = Tk()
root.geometry("900x600")
root.title('Laboratory Information Management System LIMS')

#ikkunan alueet

frame1 =Frame(root, width=300,bg="azure")
frame1.pack(fill=BOTH, side=LEFT, expand=True)
nayte_teksti = Label(frame1, text = "Käyttäjän tiedot:",bg="azure")
nayte_teksti.pack(side=TOP, padx=100)

käyttäjä_label = Label(frame1, text = kayttajat[0],bg="azure")
käyttäjä_label.pack()
käyttäjä_rooli = Label(frame1, text = rooli,bg="azure")
käyttäjä_rooli.pack()


frame2 =Frame(root,width=300,bg="LightBlue1")
frame2.pack(fill=BOTH, side=LEFT,expand=True)
nayte_teksti = Label(frame2, text = "Näytteet:", bg="LightBlue1")
nayte_teksti.pack(side=TOP, padx=100)


frame3 =Frame(root, width=300, bg="SkyBlue")
frame3.pack(fill=BOTH, side=LEFT,expand=True)
nayte_teksti = Label(frame3, text = "Tulokset:", bg="SkyBlue")
nayte_teksti.pack(side=TOP, padx=100)




####### funktiot ##########


def syötäTulos():
   
    teksti_valikossa = "Valitse tästä"
    tulosvalinta = []
    for näyte in tulokset:
        tulosvalinta.append(näyte)

    syöttöikkuna = Tk()
    syöttöikkuna.geometry("600x300")
    syöttöikkuna.title('Syötä tulos')
    syötä_teksti = Label(syöttöikkuna, text="Valitse näyte valikosta")
    syötä_teksti.pack()
    alasveto = StringVar(syöttöikkuna)
    alasveto.set(teksti_valikossa) # alkuteksti

    valikko = OptionMenu(syöttöikkuna, alasveto, *tulosvalinta)
    valikko.pack()
    haettu_näyte = ""

    def valinta():
        
        haettu_näyte = alasveto.get()

        testi= simpledialog.askstring(title=haettu_näyte, prompt="Anna testin nimi:")
        #tarkistetaan ylikirjoitetaanko tulos
        if testi in tulokset[haettu_näyte]["tulokset"]:
            
            if tulokset[haettu_näyte]["tulokset"][testi] != "" or tulokset[haettu_näyte]["tulokset"][testi] != None:
                #tkinter.messagebox.showwarning('Näytteen testillä jo tulos!', "Testillä on jo tulos!")
                response=messagebox.askquestion("Testillä on jo tulos ","Haluatko ylikirjoittaa tuloksen?", 
                icon='warning')
                if response == "no":
                    return
        tulos= simpledialog.askstring(title=testi, prompt="Anna testin tulos:")
        
        #testaan ettei tyhjää sekä ettei cancelia paineta (None)
        if testi != "" and tulos != "":
            if testi != None and tulos != None:
                tulokset[haettu_näyte]["tulokset"][testi] = tulos
            else:
                tkinter.messagebox.showwarning('Tuloksen syöttö ei onnistunut', "Painoit cancelia tai et syöttänyt testin nimeä tai tulosta!")
        else:
            tkinter.messagebox.showwarning('Tuloksen syöttö ei onnistunut', "Painoit cancelia tai et syöttänyt testin nimeä tai tulosta!")
        #päivitetään tulosnäkymä
        tulosta_tulos_nappulasta(haettu_näyte)
        #lokikirja
        aika = str(datetime.now())
        teko = f"lisäsi näytteelle {haettu_näyte} testin {testi} ja tuloksen {tulos},"
        tallenna_lokiin(lokikirja,kayttajat[0],aika,teko)
        syöttöikkuna.destroy()
        #return haettu_näyte

    
    button = Button(syöttöikkuna, text="OK", command= lambda: valinta())
    button.pack()



def tulostaTulokset():

    #tyhjennetään listaus
    for label in frame3.pack_slaves():
        label.destroy()

    #tulosteen Tulokset-teksti takaisin
    nayte_teksti = Label(frame3, text = "Tulokset:", bg="SkyBlue")
    nayte_teksti.pack(side=TOP, padx=100)
    
    haettu_näyte = simpledialog.askstring(title="Tulosta näytteen tulokset", prompt="Anna näytteen nimi:")
    if haettu_näyte not in tulokset:
        tkinter.messagebox.showwarning('Näytettä ei löydy', "Kirjastosta ei löydy näytettä tällä nimellä!")
    
    elif haettu_näyte in tulokset and len(tulokset[haettu_näyte]["tulokset"]) == 0:
        tkinter.messagebox.showwarning('Näytteellä ei ole tuloksia', "Näytteelle ei ole kirjattu vielä tuloksia!")
    else:
        
        label_i = Label(frame3, text=f'{haettu_näyte}', bg="SkyBlue")
        label_i.pack()
        


        for näyte in tulokset:
            if haettu_näyte == näyte:
                for tulos in tulokset[näyte]:
                    ii = 1
                    for testi in tulokset[näyte][tulos]:
                        label_i = Label(frame3, text=f"{testi}: {tulokset[näyte][tulos][testi]}",bg="SkyBlue")
                        label_i.pack()
                        ii +=1
                        

    

def tulosta_tulos_nappulasta(näyte_parametri):
    
    #tyhjennetään listaus
    for label in frame3.pack_slaves():
        label.destroy()

    #tulosteen Tulokset-teksti takaisin
    nayte_teksti = Label(frame3, text = f"Tulokset:", bg="SkyBlue")
    nayte_teksti.pack(side=TOP, padx=100)

    label_i = Label(frame3, text=f'{näyte_parametri}',bg="SkyBlue")
    
    label_i.pack()
    for tulos in tulokset[näyte_parametri]:
        ii = 1
        for testi in tulokset[näyte_parametri][tulos]:
            label_i = Label(frame3, text=f"{testi}: {tulokset[näyte_parametri][tulos][testi]}",bg="SkyBlue")
            label_i.pack()
            ii +=1
    #Jos ei tuloksia:
    if len(tulokset[näyte_parametri]["tulokset"]) == 0:
        label_ei_tuloksia = Label(frame3,text=f"Näytteellä {näyte_parametri} ei ole vielä tuloksia",bg="SkyBlue")
        label_ei_tuloksia.pack()


# näytteen funktiot

def tulostaNäytteet(tulokset:dict):
    

    #tyhjennetään listaus
    for label in frame2.pack_slaves():
        label.destroy()
    
    nayte_teksti = Label(frame2, text = f"Näytteet", bg="LightBlue1")
    nayte_teksti.pack(side=TOP, padx=100)

    

    for näyte in tulokset:
        näytteen_nimi = näyte
        
        action_with_arg = partial(tulosta_tulos_nappulasta, näytteen_nimi)
        button_i = Button(frame2, text=näyte, command= action_with_arg)
    
        button_i.pack()
        

    
def poista():
    tkinter.messagebox.showwarning('Poistaminen ei ole sallittua!', "Näytettä tai tulosta ei voi poistaa, koska tämä vaarantaa tulosten jäljitettävyyden!")

def lisääNäyte():
    näyte = simpledialog.askstring(title="Lisää näyte", prompt="Anna näytteen nimi:")
    if näyte in tulokset:
        tkinter.messagebox.showwarning('Näytenimi on jo olemassa', "Nimi ei kelpaa: toisella näytteellä on jo sama nimi!")
    elif näyte == None or näyte =="":
        tkinter.messagebox.showwarning('Näytettä ei lisätty!', "Painoit cancel tai annoit tyhjän merkkijonon!")
    else:
        
        tulokset[näyte] = {}
        tulokset[näyte]["tulokset"] = {}
        #lokikirjaa varten tiedot:
        aika = str(datetime.now())
        teko = f"lisäsi näytteen nimellä {näyte},"

        tallenna_lokiin(lokikirja,kayttajat[0],aika,teko)
        tulostaNäytteet(tulokset)


def lataa_näytteet(sanakirja:dict):
    
    #tyhjennetään sanakirja, jotta edelliset tulokset eivät kummittele
    sanakirja.clear()
    try:
        nimi = simpledialog.askstring(title="Lataa näytetiedot tiedostosta", prompt="Anna tiedoston nimi päätteen kanssa (esim. tiedosto.txt):")
        file = open(nimi, "r",encoding='utf-8')  #
    except FileNotFoundError:
        tkinter.messagebox.showwarning('Tiedostoa ei löydy!', "Antamallasi nimellä ei löydy tiedostoa, kokeile uudelleen!")
    contents = file.read()
    sanakirja1 = ast.literal_eval(contents)
    file.close()
    sanakirja.update(sanakirja1)
    #tulostetaan näkyviin mikä tiedosto ladattiin
    tulosta_tiedot(nimi)
    #tulostetaan näytteet näkyviin
    tulostaNäytteet(sanakirja) 
    
    return sanakirja


def tallenna_näytteet(sanakirja:dict):
    nimi = simpledialog.askstring(title="Tallenna näytetiedot tiedostoon", prompt="Anna tiedoston nimi päätteen kanssa (esim. tiedosto.txt):")
    with open(nimi, 'w',encoding='utf-8') as f:
        print(sanakirja, file=f)

#käyttäjän ja tiedot funktiot

def tulosta_tiedot(haettu_näytekirjasto):
    
    
    for label in frame1.pack_slaves():
        label.destroy()
    nayte_teksti = Label(frame1, text = "Käyttäjän tiedot:",bg="azure")
    nayte_teksti.pack(side=TOP, padx=100)
    #käyttäjän tiedot
    käyttäjä_label = Label(frame1, text = kayttajat[0],bg="azure")
    käyttäjä_label.pack()
    käyttäjä_rooli = Label(frame1, text = rooli,bg="azure")
    käyttäjä_rooli.pack()
    näytetiedosto_label = Label(frame1,text=f"Hait näytteet: {haettu_näytekirjasto}",bg="azure")
    näytetiedosto_label.pack()

def vaihda_käyttäjä(kayttaja):
    vanha_kayttaja = kayttajat[0]
    kayttaja = simpledialog.askstring(title="Tallenna näytetiedot tiedostoon", prompt="Anna nimi:")
    kayttajat[0] = kayttaja
    for label in frame1.pack_slaves():
        label.destroy()
    nayte_teksti = Label(frame1, text = "Käyttäjän tiedot:",bg="azure")
    nayte_teksti.pack(side=TOP, padx=100)
    #käyttäjän tiedot
    käyttäjä_label = Label(frame1, text = kayttaja,bg="azure")
    käyttäjä_label.pack()
    käyttäjä_rooli = Label(frame1, text = rooli,bg="azure")
    käyttäjä_rooli.pack()
    #lokikirjaa varten tiedot:
    aika = str(datetime.now())
    teko = f"vaihdettiin käyttäjäksi henkilön {vanha_kayttaja} toimesta,"

    tallenna_lokiin(lokikirja,kayttajat[0],aika,teko)
    


# Näytehistorian funktiot

def tallenna_lokiin(lokikirja:dict,kayttaja, aika:date, teko:str):
    lause = kayttaja +" " +teko + " pvm ja klo: " + str(aika)
    lokikirja.append(lause)
    with open("lokikirja.txt", 'a',encoding='utf-8') as f:  #jatkossa voisi olla eri lokikirjoja, mutta toisaalta käyttäjän ei pitäisi päästä siihen käsiksi
        for teko in lokikirja:
            f.write(teko + "\n")

def tulostaLokikirja():
    
    nimi = simpledialog.askstring(title="Lue lokikirjan merkinnät", prompt="Anna tiedoston nimi päätteen kanssa (esim. tiedosto.txt):")
    
    try:
        #testataan onko filename ok, ei tehdä mitään:
        with open(nimi, 'r',encoding='utf-8') as f:
            f.read()
        #oma ikkuna tuloksille
        oma_ikkuna = Tk()
        oma_ikkuna.title('Lokikirjan merkinnät')
        S = Scrollbar(oma_ikkuna)
        T = Text(oma_ikkuna, height=40, width=100)
        S.pack(side=RIGHT, fill=Y)
        T.pack(side=LEFT, fill=Y)
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
    
        with open(nimi, 'r',encoding='utf-8') as f:
            for teko in f:
                T.insert(END, teko)

    except FileNotFoundError:
        tkinter.messagebox.showwarning('Tiedostoa ei löydy!', "Antamallasi nimellä ei löydy tiedostoa, kokeile uudelleen!")
        return
    
    lokikirja_tiedosto = nimi
    lokikirjan_label = Label(frame1,text=f"Lokikirja: {lokikirja_tiedosto}",bg="azure")
    lokikirjan_label.pack()




def testin_kaikki_tulokset():
    eri_testit = []
    for näyte in tulokset:
        for testi in tulokset[näyte]["tulokset"]:
            if testi not in eri_testit:
                eri_testit.append(testi)
    
    teksti_valikossa = "Valitse tästä"
    

    syöttöikkuna = Tk()
    syöttöikkuna.geometry("600x300")
    syöttöikkuna.title('Valitse testi')
    syötä_teksti = Label(syöttöikkuna, text="Valitse testi valikosta")
    syötä_teksti.pack()
    alasveto = StringVar(syöttöikkuna)
    alasveto.set(teksti_valikossa) # alkuteksti

    valikko = OptionMenu(syöttöikkuna, alasveto, *eri_testit)
    valikko.pack()
    

    def valinta_testi():
        
        print("nyt valinta funktiossa")
        haettu_testi = alasveto.get()
        print("Valittiin: " + haettu_testi)
        syöttöikkuna.destroy()
        testi_tulos_ikkuna = Tk()
        testi_tulos_ikkuna.title('Testin kaikki tulokset')
        S = Scrollbar(testi_tulos_ikkuna)
        T = Text(testi_tulos_ikkuna, height=40, width=100)
        S.pack(side=RIGHT, fill=Y)
        T.pack(side=LEFT, fill=Y)
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        T.insert(END, f"Testin {haettu_testi} kaikki tulokset:")
        T.insert(END, "\n")
        for näyte in tulokset:
            for testi in tulokset[näyte]:
                if haettu_testi in tulokset[näyte]["tulokset"]:
                    T.insert(END, f"Näyte: {näyte}, tulos: ")
                    T.insert(END,tulokset[näyte]["tulokset"][haettu_testi]) #tulos
                    T.insert(END,"\n")
        
    button = Button(syöttöikkuna, text=f"OK", command= lambda: valinta_testi())
    button.pack()


##### Ohje-valikon funktiot

def tulostaOhje():
    ohje_ikkuna = Tk()
    ohje_ikkuna.title('Käyttöohje')
    S = Scrollbar(ohje_ikkuna)
    T = Text(ohje_ikkuna, height=40, width=140)
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=LEFT, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    try:
        with open("readme.txt", 'r',encoding='utf-8') as f:
            for teko in f:
                T.insert(END, teko)
    except FileNotFoundError:
        tkinter.messagebox.showwarning('Tiedostoa ei löydy!', "Antamallasi nimellä ei löydy tiedostoa, kokeile uudelleen!")
        return

#menubar

menu = Menu(root)
root.config(menu=menu)
subMenu = Menu(menu)

## menubar: Tiedosto

tiedosto_menu = Menu(menu)
menu.add_cascade(label="Tiedosto", menu=tiedosto_menu)
tiedosto_menu.add_command(label="Hae näytteet tiedostosta", command= lambda: lataa_näytteet(tulokset))
tiedosto_menu.add_command(label="Tallenna näytteet tiedostoon", command= lambda: tallenna_näytteet(tulokset))
tiedosto_menu.add_command(label="Vaihda käyttäjää", command= lambda: vaihda_käyttäjä(kayttaja))


## menubar: Näyte
menu.add_cascade(label="Näyte", menu=subMenu)
subMenu.add_command(label="Lisää näyte", command= lambda: lisääNäyte())
subMenu.add_command(label="Syötä tulos", command=syötäTulos)
subMenu.add_separator() #viiva
subMenu.add_command(label="Tulosta näytteet", command= lambda: tulostaNäytteet(tulokset))
subMenu.add_command(label="Tulosta tulokset", command= lambda: tulostaTulokset())
subMenu.add_separator() #viiva
subMenu.add_command(label="Poista näyte/tulos", command= lambda: poista())

#menubar: Näytehistoria

historiaMenu = Menu(menu)
menu.add_cascade(label="Näytehistoria", menu=historiaMenu)
historiaMenu.add_command(label="Tulosta lokikirja", command= lambda: tulostaLokikirja())
historiaMenu.add_command(label="Tulosta testin kaikki tulokset", command= lambda: testin_kaikki_tulokset())

#menubar readme

readmeMenu = Menu(menu)
menu.add_cascade(label="Info", menu=readmeMenu)
readmeMenu.add_command(label="Lue käyttöohje", command= lambda: tulostaOhje())

root.mainloop()
