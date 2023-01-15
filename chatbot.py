import tkinter as tk
# from PIL import Image, ImageTk
import os
from tkinter import *
from functools import partial

import FoodRecommendation

ss = FoodRecommendation.FoodRecommendation()


cuisines_s = []
allergies_s = []
mood_s = []
recommendations_s = []
root = tk.Tk()
root.title("Mood Taste Foodie Hub")
# root.minsize(700, 300)
root.geometry("700x320")

# set maximum window size value
# root.maxsize(700, 300)
sick = []
cuisines = []
mood = []
recommendations_list = []
v = tk.IntVar()
# v.set(1)  # initializing the choice, i.e. Python
score = []
total_rating = 0

def calculate(x):
    
    global score 
    score.append(x)
    total_rating = sum(score)/len(score)
    print("Rating:",total_rating)

# is_on = False
my_label = Label(root,
    text = "Do you have any food allergies?",
    fg = "green",
    font = ("Helvetica", 32))
my_label.pack(pady = 20)



def Simpletoggle():
    
    if toggle_button.config('text')[-1] == 'YES':
        # toggle_button.config(image=off)
        toggle_button.config(text='NO',bg="red",fg="white")
        
    else:
        # toggle_button.config(image=on)
        toggle_button.config(text='YES',bg="green",fg="white")
        allergies_check()
       

# on = PhotoImage(file ="C:\\Users\\user\\Documents\\Term2\\on-nobg.gif")
# on = on.subsample(5,5)
# off = PhotoImage(file ="C:\\Users\\user\\Documents\\Term2\\off-nobg.gif")
# off = off.subsample(5,5)
# Create A Button


toggle_button = Button(text="NO", command=Simpletoggle,bg="red",fg="white")
toggle_button.pack(pady=10)


def ShowChoice():
    print(v.get())
    return v.get()


def getChecked():
    values = [var.get() for var in sick if var.get()]
    allergies_s = values
    print(", ".join(values))
    return ", ".join(values)

def getChecked_cuisine(): 
    values = [var.get() for var in cuisines if var.get()]
    cuisines_s = values
    print(", ".join(values))
    return ", ".join(values)
    
def getChecked_mood(): 
    values = [var.get() for var in mood if var.get()]
    mood_s = values
    print("mood:", ", ".join(values))
    
def getChecked_recomm(): 
    values = [var.get() for var in recommendations_list if var.get()]
    recommendations_s = values
    print("recommendations:", ", ".join(values))



def allergies_check():
    
    for i in range(50):
        option = StringVar(value="")
        sick.append(option)
    
    allergies_list = ['nut allergy','milk allergy / lactose intolerance','stone fruit allergy','cruciferous allergy']
   
       # Conditions checkbutton
    # frame = Frame(root)
    tk.Label(root, 
             text="""Are you allergic to any of the following?""",
             justify = tk.LEFT,
             padx = 20).pack()
             #Oral Allergy Syndrome,
    for i, item in enumerate(allergies_list):
       a = tk.Checkbutton(root, text=item, variable=sick[i],onvalue=item, offvalue="").pack()
       
    # tk.Checkbutton(root, text="Sea food", variable=sick[0],onvalue="Sea food", offvalue="").pack()
    
    # tk.Checkbutton(root, text="Lactose", variable=sick[1],onvalue="Lactose", offvalue="").pack()
    # tk.Checkbutton(root, text="Nut Allergy", variable=sick[2],onvalue="Nut Allergy", offvalue="").pack()
    # Button(root, text='Submit', command=getChecked, width=20, bg='brown', fg='white').pack()
    # Button(root, text='Next', command=lambda: [register(), getChecked()], width=20, bg='brown', fg='white').pack()

def place_order():
    for i in root.winfo_children():
        i.destroy()
    
    tk.Label(root, 
             text="""Your order has been placed!""",
             justify = tk.LEFT,
             padx = 20).pack()
    tk.Label(root, 
             text="""Thank you!""",
             justify = tk.LEFT,
             padx = 20).pack()
    Label(root, text="Please rate us ", font=("arial ", 12) ).pack()
    one = Button(root,command = partial(calculate, 1), text="1", borderwidth=3, relief="raised", padx=5, pady=10, bg="yellow").pack(anchor=CENTER)

    two = Button(root,command = partial(calculate, 2), text="2", borderwidth=3, relief="raised", padx=10, pady=10, bg="yellow").pack(anchor=CENTER)

    three = Button(root,command = partial(calculate, 3), text="3", borderwidth=3, relief="raised", padx=15, pady=10, bg="yellow").pack(anchor=CENTER)

    four = Button(root,command = partial(calculate, 4), text="4", borderwidth=3, relief="raised", padx=20, pady=10, bg="yellow").pack(anchor=CENTER)

    five = Button(root,command = partial(calculate, 5), text="5", borderwidth=3, relief="raised", padx=25, pady=10, bg="yellow").pack(anchor=CENTER)

    exit_button = Button(root, text="Exit", command=root.destroy,bg="red",fg="white")
    exit_button.pack(pady=20)

def recommendations(input):
    for i in root.winfo_children():
        i.destroy()
    for i in range(20):
        option = StringVar(value="")
        recommendations_list.append(option)

   # Conditions checkbutton
    tk.Label(root, 
             text="""Here are our best recommendations!""",
             justify = tk.LEFT,
             padx = 20).pack()
    ip_list = input
    for i, item in enumerate(ip_list):
        tk.Checkbutton(root, text=item, variable=recommendations_list[i],onvalue=item, offvalue="").pack()
    # Button(root, text='Next', command=lambda: [getChecked_recomm()], width=20, bg='brown', fg='white').pack()
    Button(root, text='Place Order', command=lambda: [place_order(),getChecked_recomm()], width=20, bg='green', fg='white').pack()


def mood_check():
    
    for i in root.winfo_children():
        i.destroy()
    for i in range(20):
        option = StringVar(value="")
        mood.append(option)

   # Conditions checkbutton
    tk.Label(root, 
             text="""What are you in the mood to eat?""",
             justify = tk.LEFT,
             padx = 20).pack()
    tk.Checkbutton(root, text="spicy", variable=mood[0],onvalue="spicy", offvalue="").pack()

    tk.Checkbutton(root, text="mild", variable=mood[1],onvalue="mild", offvalue="").pack()
    tk.Checkbutton(root, text="saucy", variable=mood[2],onvalue="saucy", offvalue="").pack()
    Button(root, text='Next', command=lambda: [getChecked_mood(), recommendations(get_food_recomm())], width=20, bg='brown', fg='white').pack() 

def get_food_recomm():
    rec = ss.get_recommendation([getChecked()], [getChecked_cuisine()])
    recomm_id = rec['name']
    return list(recomm_id)

#method for returning id of the recommended food items
def get_food_recomm_id():
    rec = ss.get_recommendation([getChecked()], [getChecked_cuisine()])
    names = rec['Unnamed: 0']
    return list(names)


def register():
    
    for i in root.winfo_children():
        i.destroy()
    for i in range(20):
        option = StringVar(value="")
        cuisines.append(option)

   # Conditions checkbutton
    tk.Label(root, 
             text="""What do you feel like eating?""",
             justify = tk.LEFT,
             padx = 20).pack()
             
    tk.Checkbutton(root, text="non-veg", variable=cuisines[0],onvalue="non-veg", offvalue="").pack()
    tk.Checkbutton(root, text="veg", variable=cuisines[1],onvalue="veg", offvalue="").pack()
    tk.Checkbutton(root, text="european", variable=cuisines[2],onvalue="european", offvalue="").pack()
    tk.Checkbutton(root, text="indian", variable=cuisines[3],onvalue="indian", offvalue="").pack()
    tk.Checkbutton(root, text="japanese", variable=cuisines[4],onvalue="japanese", offvalue="").pack()
    
    # Button(root, text='Submit', command=getChecked_cuisine, width=20, bg='brown', fg='white').pack()
    Button(root, text='Next', command=lambda: [mood_check(), getChecked_cuisine(),get_food_recomm(),get_food_recomm_id()], width=20, bg='brown', fg='white').pack()
    
    # register_btn = tk.Button(text="Next", command=mood_check)
    # register_btn.pack(side=BOTTOM)


register_btn = tk.Button(text="Next", command=lambda: [register(), getChecked()], width=20, bg='brown', fg='white')
register_btn.pack(side=BOTTOM)



root.mainloop()