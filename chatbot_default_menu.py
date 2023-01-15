import tkinter as tk
from tkinter import *
import pandas as pd

data = pd.read_csv('recipe_preprocessed.csv')

op = data['name'] + "   -   " +  data['allergy']
root = tk.Tk()
root.title("Mood Taste Foodie Hub")

recommendations_list = []
recommendations_s = []




def getChecked_recomm(): 
    values = [var.get() for var in recommendations_list if var.get()]
    recommendations_s = values
    print("recommendations:", ", ".join(values))


def recommendations():
    for i in root.winfo_children():
        i.destroy()
    for i in range(40):
        option = StringVar(value="")
        recommendations_list.append(option)
   
    tk.Label(root, 
            text="""Menu""",
            justify = tk.LEFT,
            padx = 20,bg="red",fg="white").pack()
    ip_list = op
    for i, item in enumerate(ip_list):
        tk.Checkbutton(root, text=item, variable=recommendations_list[i],onvalue="id: "+ str(i)+ ",item: " +item, offvalue="").pack()
    Button(root, text='Place Order', command=lambda: [getChecked_recomm()], width=20, bg='green', fg='white').pack()
    tk.Label(root, 
            text="""S - stone fruit allergy | N - nut allergy | M - milk allergy / lactose intolerance | C - cruciferous allergy """,
            justify = tk.LEFT,
            padx = 20,bg="blue",fg="white").place(x=900,y=50)



    

recommendations()

root.mainloop()