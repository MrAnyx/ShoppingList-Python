from tkinter import *
from tkinter import ttk #pour les combobox
from tkinter import messagebox
import sqlite3 as sql
import datetime

####################################################

def select_aliment(): #permet d'ajourer un element dans la liste de course
	try:
		var = listebox_all.get(listebox_all.curselection())
		liste = var.split(' | ')
		cursor.execute("""INSERT INTO LISTE_COURSE (type, aliment, magasin) VALUES (?, ?, ?)""", (liste[0], liste[1], liste[2]))
		db.commit()
		actualiser_liste()
	except:
		messagebox.showerror("Erreur | Selection aliment", "Veuillez selectionner un aliment avant de le déplacer")

def export(): #pour exporter la liste avec un beau format en .txt dans le OneDrive (faire un groupe by en fonction du type) !!!
	try:
		showtime = datetime.datetime.now().strftime("%d - %m - %Y")
		fichier = open("Path you want", "w")

		fichier.write(125*"-" + "\n")
		fichier.write("|" + 63*" " + " " + showtime + " " + 63*" " + "|" + "\n")
		fichier.write(125*"-" + "\n")

		fichier.write("\n\n\n")
		cursor.execute("""SELECT type, aliment, magasin FROM LISTE_COURSE ORDER BY type""")
		liste = cursor.fetchall()
		for i in liste:
			fichier.write("{} | {} ({})\n".format(i[0], i[1], i[2]))

		fichier.close()
		messagebox.showinfo("Info | Exportation", "Exportation réussie")
	except:
		messagebox.showerror("Erreur | Exportation", "Erreur lors de l'exportation\nVeuillez ré-essayer")

def ajouter(): #pour ajouter un element dans la liste all
	if(value_type.get() != "" and value_aliment.get() != "" and value_magasin.get() != ""):
		cursor.execute("""INSERT INTO LISTE_ALL (type, aliment, magasin) VALUES (?, ?, ?)""", (value_type.get(), value_aliment.get(), value_magasin.get()))
		db.commit()
		actualiser()
		raz()
	else:
		messagebox.showerror("Erreur | Ajout aliment", "Veuillez remplir l'ensemble des champs de saisis\nde la rubrique 'Ajouter' puis ré-essayez")

def raz(): #pour mettre a zero la liste de course
	value_type.set("")
	value_search.set("")
	value_aliment.set("")
	value_magasin.set("")

def remove_all(): # permet de supprimer un element de la liste all
	try:
		var = listebox_all.get(listebox_all.curselection())
		liste = var.split(' | ')
		cursor.execute("""DELETE FROM LISTE_ALL WHERE type LIKE "%{}%" AND aliment LIKE "%{}%" AND magasin LIKE "%{}%" """.format(liste[0], liste[1], liste[2]))
		db.commit()
		actualiser_all()
	except:
		messagebox.showerror("Erreur | Suppr liste all", "Selectionnez un élément avant de le supprimer")


def remove_liste(): # permet de supprimer un element de la liste all
	try:
		var = listebox_liste.get(listebox_liste.curselection())
		liste = var.split(' | ')
		cursor.execute("""DELETE FROM LISTE_COURSE WHERE type LIKE "%{}%" AND aliment LIKE "%{}%" AND magasin LIKE "%{}%" """.format(liste[0], liste[1], liste[2]))
		db.commit()
		actualiser_liste()
	except:
		messagebox.showerror("Erreur | Suppr liste courses", "Selectionnez un élément avant de le supprimer")

def trier(): # pour trier la liste_all en fonction d'un champ et de la combobox
	if(value_search.get()!=""):	
		listebox_all.delete(0, END)
		if(combobox.get() == ""):
			actualiser_all()
		else:
			cursor.execute("""SELECT type, aliment, magasin FROM LISTE_ALL WHERE {} LIKE "%{}%" """.format(combobox.get(), value_search.get()))
			liste = cursor.fetchall()
			if(len(liste) >0):
				for i in liste:
					listebox_all.insert(END, "{} | {} | {}".format(i[0], i[1], i[2]))
				raz()
			else:
				actualiser_all()
				raz()
				messagebox.showwarning("Warning | Tri", "La valeur entrée n'existe pas\n Veuillez ré-essayer")
				
	else:
		messagebox.showerror("Erreur | Tri", "Veuillez remplir le champ de saisis avant de trier")


def actualiser_liste(): # actualise la liste
	listebox_liste.delete(0, END)
	affiche_liste()

def actualiser_all(): # actualise la liste
	listebox_all.delete(0, END)
	affiche_all()

def actualiser():
	actualiser_all()
	actualiser_liste()

def clear_liste(): #détruit la liste de course en cours
	cursor.execute("""DELETE FROM LISTE_COURSE""")
	db.commit()
	actualiser_liste()
	messagebox.showinfo("Info | Clear liste de course", "La liste de course a bien été réinitialisée")

def affiche_all(): #affiche la liste de gauche
	cursor.execute("""SELECT type, aliment, magasin FROM LISTE_ALL""")
	liste = cursor.fetchall()
	for i in liste:
		listebox_all.insert(END, "{} | {} | {}".format(i[0], i[1], i[2]))

def affiche_liste(): #affiche la liste de droite
	cursor.execute("""SELECT type, aliment, magasin FROM LISTE_COURSE""")
	liste2 = cursor.fetchall()
	for j in liste2:
		listebox_liste.insert(END, "{} | {} | {}".format(j[0], j[1], j[2]))



####################################################
db = sql.connect("database.db")
cursor = db.cursor()

cursor.execute("""
	CREATE TABLE IF NOT EXISTS LISTE_ALL(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	type TEXT NOT NULL,
	aliment TEXT NOT NULL,
	magasin TEXT NOT NULL
	)
""")

cursor.execute("""
	CREATE TABLE IF NOT EXISTS LISTE_COURSE(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	type TEXT NOT NULL,
	aliment TEXT NOT NULL,
	magasin TEXT NOT NULL
	)
""")

####################################################
fenetre = Tk()
fenetre.resizable(width = False, height = False)
fenetre.title("Liste Courses")
fenetre.configure(bg = "#969696")
fenetre.iconbitmap("1.ico")

####################################################
frame1 = LabelFrame(fenetre, bg = "#969696")


listebox_all = Listbox(frame1, width = 26)
affiche_all()
listebox_all.pack(side = LEFT, fill = X, expand = 1, padx = (12,0), pady = 10)

scrollbar1 = Scrollbar(frame1)
scrollbar1.pack(side = LEFT, fill = Y, expand = 1, padx = (0,12), pady = 10)

listebox_all.configure(yscrollcommand = scrollbar1.set)
scrollbar1.config(command = listebox_all.yview)

############

bouton = Button(frame1, bg = "#515151", fg = "white", text = ">", font = ("", 15), width = 3, command = select_aliment).pack(side = LEFT,expand = 1)

############

listebox_liste = Listbox(frame1, width = 26)
affiche_liste()
listebox_liste.pack(side = LEFT, fill = X, expand = 1, padx = (12,0), pady = 10)

scrollbar2 = Scrollbar(frame1)
scrollbar2.pack(side = LEFT, fill = Y, expand = 1, padx = (0,12), pady = 10)

listebox_liste.configure(yscrollcommand = scrollbar2.set)
scrollbar2.config(command = listebox_liste.yview)

frame1.pack(fill = X, padx = 5, pady = (5,0))
####################################################
frame2 = LabelFrame(fenetre, bg = "#969696", text = "Ajouter")

value_type = StringVar()
value_aliment = StringVar()
value_magasin = StringVar()
entry_type = Entry(frame2, textvariable = value_type, font = ("", 12), bg = "bisque", selectforeground = "red", selectbackground = "bisque", width = 10).pack(side = LEFT, fill = X, expand = 1, padx = 10, pady = (3,13))
entry_aliment = Entry(frame2, textvariable = value_aliment, font = ("", 12), bg = "bisque", selectforeground = "red", selectbackground = "bisque", width = 10).pack(side = LEFT, fill = X, expand = 1, pady = (3,13))
entry_magasin = Entry(frame2, textvariable = value_magasin, font = ("", 12), bg = "bisque", selectforeground = "red", selectbackground = "bisque", width = 10).pack(side = LEFT, fill = X, expand = 1, padx = 10, pady = (3,13))


frame2.pack(fill = X, padx = 5, pady = (5,0))
####################################################
frame3 = LabelFrame(fenetre, bg = "#969696", text = "Trier")

value_search = StringVar()
entry_search = Entry(frame3, textvariable = value_search, bg = "bisque", font = ("", 12), selectbackground = "bisque", selectforeground = "red", width = 22).pack(side = LEFT, fill = X, expand = 1, padx = 10, pady = (3,13))

combobox = ttk.Combobox(frame3, font = ("", 12), state="readonly")
combobox['values'] = ("", "Type", "Aliment", "Magasin")
combobox.pack(side = LEFT, fill = X,expand = 1, padx = (0,10), pady = (3,13))

frame3.pack(fill = X, padx = 5, pady = (5,0))
####################################################
frame4 = LabelFrame(fenetre, bg = "#969696", text = "Interaction")

bouton3 = Button(frame4, text = "Ajouter", bg = "#515151", fg = "white", font = ("", 12), command = ajouter).pack(side = LEFT, fill = X,expand = 1, padx = 10, pady = (3,13))
bouton4 = Button(frame4, text = "Trier", bg = "#515151", fg = "white", font = ("", 12), command = trier).pack(side = LEFT, fill = X,expand = 1, padx = (0,10), pady = (3,13))

frame4.pack(fill = X, padx = 5, pady = (5,5))

####################################################
menubar = Menu(fenetre)
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label="Export", command=export)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=fenetre.destroy)
menubar.add_cascade(label="File", menu=filemenu)

edit = Menu(menubar, tearoff = 0)
edit.add_command(label="Remove From All", command = remove_all)
edit.add_command(label="Remove From Liste", command = remove_liste)
edit.add_separator()
edit.add_command(label="Refresh", command = actualiser)
edit.add_command(label="Clear List", command = clear_liste)
edit.add_separator()
edit.add_command(label="RaZ", command = raz)
menubar.add_cascade(label = "Edit", menu = edit)
fenetre.config(menu = menubar)

####################################################
fenetre.mainloop()
db.close()
