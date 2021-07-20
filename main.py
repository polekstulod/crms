import tkinter as tk
from tkinter.constants import ANCHOR
from PIL import ImageTk,Image
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import sqlite3

def main():
    root = tk.Tk()
    Login(root)
    root.mainloop()
       
def logout(master):
    master.withdraw()
    toplevel = tk.Toplevel()
    Login(toplevel)
    
def change_window(master, frame):
    master.withdraw()
    toplevel = tk.Toplevel()  
    if frame == "MainMenu":
        MainMenu(toplevel)
    elif frame == "RecipePage":
        RecipePage(toplevel)
    elif frame == "AddRecipePage":
        AddRecipePage(toplevel)
    elif frame == "AdminPage":
        AdminPage(toplevel)
    elif frame == "SignUpPage":
        SignUp(toplevel)
    elif frame == "from_addrec":
        if accountLevel == "admin":
            AdminPage(toplevel)
        elif accountLevel == "user":
            MainMenu(toplevel)

def view_recipe(master,recname,recingr,recpro,recprice,rectime,recmealtype, directory):
    master.withdraw()
    toplevel = tk.Toplevel()
    RecipePage(toplevel,recname,recingr,recpro,recprice,rectime,recmealtype, directory)
    
    
class Recipe:
    def __init__(self, recname, recingr, recpro, recprice, rectime, recmealtype):
        self.recname = recname
        self.recingr = recingr
        self.recpro = recpro
        self.recprice = recprice
        self.rectime = rectime
        self.recmealtype = recmealtype

    def create_recipe_with_frame(self, master, root, directory):
        self.recframe = tk.Frame(master)
        self.directory = directory
        self.recimg = ImageTk.PhotoImage(Image.open(self.directory))
        self.butt = tk.Button(self.recframe, image=self.recimg, borderwidth=0,command=lambda: view_recipe(root, self.recname, self.recingr, self.recpro, self.recprice, self.rectime, self.recmealtype, self.directory))
        self.butt.image = self.recimg
        self.butt.pack()
        tk.Label(self.recframe, text=self.recname,font= ("Calibri",15,'bold')).pack(padx=10,pady=10)
        return self.recframe
    



class Login(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master,*args, **kwargs)
        self.master = master
        
        master.title("Login")
        master.geometry('1360x690+0+0')
        master.iconbitmap('icons/systemicon.ico')
        
        #Creating bg image
        self.loginbg = ImageTk.PhotoImage(Image.open('images/Loginbg.png'))
        tk.Label(master,image = self.loginbg).place(x = 0, y= 0, relwidth = 1, relheight= 1)
        
        
        #Creating a frame with label
        self.loginframe = tk.Frame(master)
        self.loginframe.pack(padx = 50, pady= 120)
        tk.Label(self.loginframe,text="WELCOME",fg = '#ea6527',font = ("Calibri",40,'bold')).grid(column=0, row = 5,padx= 50)

        #Add Logo inside the frame
        self.systemlogo = ImageTk.PhotoImage(Image.open('images/frameicon.png'))
        framelogo = tk.Label(self.loginframe,image = self.systemlogo)
        framelogo.grid(column = 0, row = 4,pady = 10)
        
        #Creating a Fill up form
        tk.Label(self.loginframe, text= 'Username',fg = '#ea6527',font = ("Calibri",20,'bold')).grid(column = 0, row = 6,pady= 10)
        username = tk.Entry(self.loginframe, width = 50)
        username.grid(column= 0, row=7,ipady = 8)

        tk.Label(self.loginframe, text= 'Password',fg= '#ea6527',font = ("Calibri",20,'bold')).grid(column = 0, row =8)
        password = tk.Entry(self.loginframe, width = 50)
        password.config(show='*')
        password.grid(column= 0, row=9,ipady = 8,pady = 10)
        
        #Creating login button
        tk.Button(self.loginframe, text= 'LOGIN',font= ("Calibri",12,'bold'),width= 20, height= 1,background = '#ea6527', command=lambda: self.login(username,password)).grid(column= 0, row= 10, padx= 20)
        
        #Creating Signup button
        tk.Button(self.loginframe, text= 'Sign Up',font= ("Calibri",12,'bold'),background = '#ea6527', command=lambda: change_window(master, "SignUpPage")).grid(column= 0, row= 11, padx= 20, pady=10)

    
    def login(self, username, password):
        global uid, accountID, accountLevel
        toplevel = tk.Toplevel(self.master)
        un = username.get()
        pw = password.get()
        conn = sqlite3.connect('DB.db')
        c = conn.cursor()

        c.execute(f"select account_status from accounts where Username = '{un}' and Password = '{pw}'")
        if not c.fetchone():
            messagebox.showwarning('', "Incorrect Credentials")
        else:
            c.execute(f"select username,Account_Status from accounts where username = '{un}' and Account_Status='admin'")
            if not c.fetchone():
                c.execute(f"select Log_In_ID,Account_Status from accounts where username = '{un}' and Account_Status='user'")
                uid = c.fetchall()
                accountLevel = uid[0][1]
                accountID = uid[0][0]
                print(accountLevel)
                MainMenu(toplevel)
                self.master.withdraw()
            else:
                c.execute(f"select Log_In_ID,Account_Status from accounts where username = '{un}' and Account_Status='admin'")
                uid = c.fetchall()
                accountID = uid[0][0]
                accountLevel = uid[0][1]
                print(accountLevel)
                AdminPage(toplevel)
                self.master.withdraw()
 
class SignUp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        
        master.title("Sign Up Page")
        master.geometry('1360x690+0+0')
        master.configure(bg='#ea6527')
        master.iconbitmap('icons/systemicon.ico')

        self.systemlogo = ImageTk.PhotoImage(Image.open('images/frameicon.png'))
        tk.Label(master,image = self.systemlogo).pack(anchor= tk.W)

        self.admintab = tk.Frame(master,bg ='#baced7',highlightbackground='white', highlightthickness = 2)
        self.admintab.pack(fill='x')
        tk.Button(self.admintab,text= 'Exit',font= ("Calibri",18),background = '#baced7',width= 15, height= 1,borderwidth= 0, command=lambda: logout(master)).pack(side=tk.RIGHT)
        tk.Label(self.admintab,text='Sign Up',font=('Calibri',18),bg='#baced7').pack(padx = 400,side=tk.RIGHT)

        self.signupframe = tk.Frame(master)
        self.signupframe.pack(fill= 'both')

        tk.Label(self.signupframe,text='First name:',font= ("Calibri",18)).grid(column=0,row=0,sticky=tk.E,padx=5,pady=40)
        tk.Label(self.signupframe,text= 'Last name:',font= ("Calibri",18)).grid(column=0,row=1,sticky=tk.E,padx=5)
        tk.Label(self.signupframe,text= 'Birthdate (MM/DD/YYYY):',font= ("Calibri",18)).grid(column=0,row=2,sticky=tk.E,padx=5,pady=40)
        tk.Label(self.signupframe,text= 'Username:',font= ("Calibri",18)).grid(column=0,row=3,sticky=tk.E,padx=5)
        tk.Label(self.signupframe,text= 'Password:',font= ("Calibri",18)).grid(column=0,row=4,sticky=tk.E,padx=5)

        self.fisrtname_entry = tk.Entry(self.signupframe, width = 50)
        self.fisrtname_entry.grid(column =1,row=0,sticky=tk.W,padx=5,pady=40,ipady=5)
        self.lastname_entry = tk.Entry(self.signupframe, width = 50)
        self.lastname_entry.grid(column =1,row=1,sticky=tk.W,padx=5,ipady=5)
        self.birthdate_entry = tk.Entry(self.signupframe, width = 50)
        self.birthdate_entry.grid(column =1,row=2,sticky=tk.W,padx=5,pady=40,ipady=5)
        self.username_entry = tk.Entry(self.signupframe, width = 50)
        self.username_entry.grid(column =1,row=3,sticky=tk.W,padx=5,ipady=5)
        self.password_entry = tk.Entry(self.signupframe, width = 50)
        self.password_entry.grid(column =1,row=4,sticky=tk.W,padx=5,pady=40,ipady=5)

        self.submitbtn = tk.Button(self.signupframe,text= 'Submit',font= ("Calibri",18),width= 15, height= 1,borderwidth= 1,background = '#ea6527', command = lambda: register(self.fisrtname_entry.get(), self.lastname_entry.get(), self.birthdate_entry.get(), self.username_entry.get(), self.password_entry.get(), master))
        self.submitbtn.grid(column=0,row=5,columnspan= 2,pady=80)

        self.signupframe.columnconfigure(0,weight=1)
        self.signupframe.columnconfigure(1,weight=1)
    
def register(firstname, lastname, birthdate, username, password, master):
        
    conn = sqlite3.connect('DB.db')
    c = conn.cursor()
    c.execute("insert into user values ('981', :firstname, :lastname, :birthdate)",
    {
        'firstname': firstname,
        'lastname': lastname,
        'birthdate' : birthdate
    })
    c.execute("insert into accounts values ('981', :username, :password, 'user')",
    {
    'username' : username,
    'password' : password
    })
    conn.commit()
    messagebox.showinfo("showinfo","Signup Complete")
    logout(master)
    conn.close()

class MainMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master

        master.configure(bg='#ea6527')
        master.title('Mainmenu')
        master.iconbitmap('icons/systemicon.ico')
        master.geometry('1360x690+0+0')
        
        #Creating logo
        self.systemlogo = ImageTk.PhotoImage(Image.open('images/frameicon.png'))
        menulogo = tk.Label(self.master,image = self.systemlogo)
        menulogo.pack(anchor=tk.W)
        
        #Creating Menu Frame and buttons
        self.menuframe = tk.Frame(master,bg ='#baced7',highlightbackground='white', highlightthickness = 2)
        self.menuframe.pack(fill='x')
        tk.Label(self.menuframe,text='Menu:   ',font=('Calibri',18),bg='#baced7').pack(side= tk.LEFT)
        tk.Button(self.menuframe,text= 'Add Recipe',font= ("Calibri",18),background = '#baced7',width= 15, height= 1,borderwidth= 0, command=lambda: change_window(master, "AddRecipePage")).pack(side=tk.LEFT)
        tk.Button(self.menuframe,text= 'Logout',font= ("Calibri",18),background = '#baced7',width= 15, height= 1,borderwidth= 0, command=lambda: logout(master)).pack(side=tk.RIGHT)
        
        #Creating scrollbar for recipes
        self.wrapper1 = tk.Frame(master)
        self.wrapper1.pack(fill="both", expand="yes")

        self.mycanvas = tk.Canvas(self.wrapper1)
        self.mycanvas.pack(side=tk.LEFT, fill="both", expand="yes")

        self.yscrollbar = ttk.Scrollbar(self.wrapper1, orient="vertical", command=self.mycanvas.yview)
        self.yscrollbar.pack(side=tk.RIGHT, fill="y")

        self.mycanvas.configure(yscrollcommand=self.yscrollbar.set)
        self.mycanvas.bind('<Configure>', lambda e: self.mycanvas.configure(scrollregion = self.mycanvas.bbox("all")))

        #Creating Recipe frame
        self.recipeframe = tk.Frame(self.mycanvas)
        self.mycanvas.create_window((0,0), window=self.recipeframe, anchor=tk.N)
        
        # Creating Label Frames for food categories
        self.breakfastframe = tk.LabelFrame(self.recipeframe, text= 'Breakfast Recipes',font= ("Calibri",20))
        self.breakfastframe.grid(column=0, row=0, sticky = "nsew")

        self.lunchframe = tk.LabelFrame(self.recipeframe, text= 'Lunch Recipes',font= ("Calibri",20))
        self.lunchframe.grid(column=0, row=1, sticky = "nsew")

        self.snackframe = tk.LabelFrame(self.recipeframe, text= 'Snack Recipes',font= ("Calibri",20))
        self.snackframe.grid(column=0, row=2, sticky = "nsew")
        
        self.dinnerframe = tk.LabelFrame(self.recipeframe, text= 'Dinner Recipes',font= ("Calibri",20))
        self.dinnerframe.grid(column=0, row=3, sticky = "nsew")

        conn = sqlite3.connect('DB.db')
        c = conn.cursor()
        c.execute("select * from Recipe where meal_type = 'Lunch' and status = 'approved'")
        info = c.fetchall()
        lunchMeals = []
        i = 0
        for x in info:
            col=[]
            for y in range(6):
                col.insert(i, x[y+1])
                i += 1
            lunchMeals.append(col)
        c.execute("select count(*) from Recipe where meal_type = 'Lunch' and status = 'approved'")
        info = c.fetchall()
        lunch_c = info[0][0]

        c.execute("select * from Recipe where meal_type = 'Breakfast' and status = 'approved'")
        info = c.fetchall()
        breakfastMeals = []
        i = 0
        for x in info:
            col=[]
            for y in range(6):
                col.insert(i, x[y+1])
                i += 1
            breakfastMeals.append(col)
        c.execute("select count(*) from Recipe where meal_type = 'Breakfast' and status = 'approved'")
        info = c.fetchall()
        breakfast_c = info[0][0]

        c.execute("select * from Recipe where meal_type = 'Dinner' and status = 'approved'")
        info = c.fetchall()
        dinnerMeals = []
        i = 0
        for x in info:
            col=[]
            for y in range(6):
                col.insert(i, x[y+1])
                i += 1
            dinnerMeals.append(col)
        c.execute("select count(*) from Recipe where meal_type = 'Dinner' and status = 'approved'")
        info = c.fetchall()
        dinner_c = info[0][0]

        c.execute("select * from Recipe where meal_type = 'Snack' and status = 'approved'")
        info = c.fetchall()
        snackMeals = []
        i = 0
        for x in info:
            col=[]
            for y in range(6):
                col.insert(i, x[y+1])
                i += 1
            snackMeals.append(col)
        c.execute("select count(*) from Recipe where meal_type = 'Snack' and status = 'approved'")
        info = c.fetchall()
        snack_c = info[0][0]

        conn.commit()
        conn.close()

        #Creating recipe frames 

        conn = sqlite3.connect('DB.db')
        c = conn.cursor()
        r = 0
        safe = 0
        for i in range(breakfast_c):
            
            c.execute("select image from Recipe where recipe_name = :name",{
            'name': breakfastMeals[i][0]
            })
            info = c.fetchall()
            photo = info[0][0]
            with open('images/'+breakfastMeals[i][0]+'.png', 'wb') as pic:
                pic.write(photo)
            ingredients = "" 
            ingredients = breakfastMeals[i][1].replace("*","\n")  
            procedure = "" 
            procedure = breakfastMeals[i][2].replace("*","\n") 
        
            Recipe(breakfastMeals[i][0],ingredients,procedure,breakfastMeals[i][3],breakfastMeals[i][4],breakfastMeals[i][5]).create_recipe_with_frame(self.breakfastframe, master, 'images/'+breakfastMeals[i][0]+'.png').grid(column=safe, row=r,padx= 135,pady=30)
            safe += 1
            if safe > 2:
                r += 1 
                safe = 0

            
        safe = 0
        for i in range(lunch_c):
            c.execute("select image from Recipe where recipe_name = :name",{
            'name': lunchMeals[i][0]
            })
            info = c.fetchall()
            photo = info[0][0]
            with open('images/'+lunchMeals[i][0]+'.png', 'wb') as pic:
                pic.write(photo) 
            ingredients = "" 
            ingredients = lunchMeals[i][1].replace("*","\n") 
            procedure = "" 
            procedure = lunchMeals[i][2].replace("*","\n")   
            Recipe(lunchMeals[i][0],ingredients,procedure,lunchMeals[i][3],lunchMeals[i][4],lunchMeals[i][5]).create_recipe_with_frame(self.lunchframe, master, 'images/'+lunchMeals[i][0]+'.png').grid(column=safe, row=r,padx= 135,pady=30)
            safe += 1
            if safe > 2:
                r += 1 
                safe = 0
        safe = 0
        for i in range(snack_c):
            c.execute("select image from Recipe where recipe_name = :name",{
            'name': snackMeals[i][0]
            })
            info = c.fetchall()
            photo = info[0][0]
            with open('images/'+snackMeals[i][0]+'.png', 'wb') as pic:
                pic.write(photo)
            ingredients = "" 
            ingredients = snackMeals[i][1].replace("*","\n")
            procedure = "" 
            procedure = snackMeals[i][2].replace("*","\n") 
            Recipe(snackMeals[i][0],ingredients,procedure,snackMeals[i][3],snackMeals[i][4],snackMeals[i][5]).create_recipe_with_frame(self.snackframe, master, 'images/'+snackMeals[i][0]+'.png').grid(column=safe, row=r,padx= 135,pady=30)
            safe += 1
            if safe > 2:
                r += 1 
                safe = 0
        safe = 0
        for i in range(dinner_c):
            c.execute("select image from Recipe where recipe_name = :name",{
            'name': dinnerMeals[i][0]
            })
            info = c.fetchall()
            photo = info[0][0]
            with open('images/'+dinnerMeals[i][0]+'.png', 'wb') as pic:
                pic.write(photo) 
            ingredients = "" 
            ingredients = dinnerMeals[i][1].replace("*","\n")
            procedure = "" 
            procedure = dinnerMeals[i][2].replace("*","\n")    
            Recipe(dinnerMeals[i][0],ingredients,procedure,dinnerMeals[i][3],dinnerMeals[i][4],dinnerMeals[i][5]).create_recipe_with_frame(self.dinnerframe, master, 'images/'+dinnerMeals[i][0]+'.png').grid(column=safe, row=r,padx= 135,pady=30)
            safe += 1
            if safe > 2:
                r += 1 
                safe = 0
        
        conn.commit()
        conn.close()


class RecipePage(tk.Frame):
    def __init__(self, master, recname, recingr, recpro, recprice, rectime, recmealtype, directory):
        tk.Frame.__init__(self, master)
        self.recname = recname
        self.recingr = recingr
        self.recpro = recpro
        self.recprice = recprice
        self.rectime = rectime
        self.recmealtype = recmealtype
        self.directory = directory
        self.master = master
        
        master.configure(bg='#ea6527')
        master.title(recname)
        master.geometry('1360x640+0+15')
        master.iconbitmap('icons/systemicon.ico')
        
        self.systemlogo = ImageTk.PhotoImage(Image.open('images/frameicon.png'))
        tk.Label(master,image = self.systemlogo).pack(anchor= tk.W)
        
        #Creating a Recipe tab
        self.recipetab = tk.Frame(master,bg ='#baced7',highlightbackground='white', highlightthickness = 2)
        self.recipetab.pack(fill='x')
        tk.Button(self.recipetab,text= 'Main Menu',font= ("Calibri",18),background = '#baced7',width= 15, height= 1,borderwidth= 0, command=lambda: change_window(master, "MainMenu")).pack(side=tk.RIGHT)
        tk.Label(self.recipetab,text=self.recname,font=('Calibri',18,'bold'),bg='#baced7').pack(side= tk.RIGHT,padx = 300)
        
        #creating scrollbar in recipe page
        self.wrapper2 = tk.Frame(master)

        self.wrapper2.pack(fill="both", expand="yes")

        self.mycanvas = tk.Canvas(self.wrapper2)
        self.mycanvas.pack(side=tk.LEFT, fill="both", expand="yes")

        self.yscrollbar = ttk.Scrollbar(self.wrapper2, orient="vertical", command=self.mycanvas.yview)
        self.yscrollbar.pack(side=tk.RIGHT, fill="y")

        self.mycanvas.configure(yscrollcommand=self.yscrollbar.set)

        self.mycanvas.bind('<Configure>', lambda e: self.mycanvas.configure(scrollregion = self.mycanvas.bbox("all")))
        
        
        #Creating Recipe details
        self.recipeframedtls = tk.Frame(self.mycanvas)
        self.mycanvas.create_window((0,0), window=self.recipeframedtls, anchor=tk.N)
        self.recipeimg = ImageTk.PhotoImage(Image.open(self.directory))
        self.recipedtlimg = tk.Label(self.recipeframedtls, image= self.recipeimg)
        self.recipedtlimg.pack(pady= 20)
        
        self.pricelbl = tk.LabelFrame(self.recipeframedtls, text= 'Recipe Price',font=('Calibri',20,'bold'))
        self.pricelbl.pack(pady=5)
        self.ingr = tk.LabelFrame(self.recipeframedtls, text= 'Ingredients',font=('Calibri',20,'bold'))
        self.ingr.pack(padx= 25,pady=2,side=tk.LEFT, anchor=tk.E)
        self.proc = tk.LabelFrame(self.recipeframedtls, text= 'Procedure',font=('Calibri',20,'bold'))
        self.proc.pack(padx= 50, pady=1,fill='x')
        
        self.pricedtls = tk.Label(self.pricelbl, text=self.recprice ,font=('Calibri',15))
        self.pricedtls.pack()
        self.ingrdtls = tk.Label(self.ingr,text=self.recingr,font=('Calibri',15))
        self.ingrdtls.pack()
        self.cookingtime = tk.Label(self.proc,text=str(self.rectime) + " minutes",font=('Calibri',15,'bold'))
        self.cookingtime.pack()
        self.procdtls = tk.Label(self.proc,text=self.recpro,font=('Calibri',15), wraplength = 800,justify = "center")
        self.procdtls.pack()


def reqRecipe(recname,recingr,recpro,recprice,rectime,recmealtype):
    conn = sqlite3.connect('DB.db')
    c = conn.cursor()
    c.execute("insert into Recipe (Recipe_Name,Recipe_Ingr,Procedure,Recipe_Price,Cooking_Time,Meal_Type,Status) values (:recname, :recingr, :recpro, :recprice, :rectime, :recMealType, 'pending')",
        {
                'recname': recname,
                'recingr': recingr,
                'recpro' : recpro,
                'recprice' : recprice,
                'rectime' : rectime,
                'recMealType': recmealtype
        })
    c.execute("insert into Recipe_Request (Account_ID,Recipe_Status) values(:userid, 'pending')",
    {
    'userid' : accountID
    })
    conn.commit()
    messagebox.showinfo("showinfo", "Recipe Pending!")
    conn.close()
    
    
def clear_text(recname,recingr,recpro,recprice,rectime,recmealtype):
    recname.delete(0, 'end')
    recingr.delete(0, 'end')
    recpro.delete(0, 'end')
    recprice.delete(0, 'end')
    rectime.delete(0, 'end')
    recmealtype.delete(0, 'end')
    

class AddRecipePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master

        master.configure(bg='#ea6527')
        master.title("Add Recipe Page")
        master.geometry('1360x690+0+0')
        master.iconbitmap('icons/systemicon.ico')
        
        self.systemlogo = ImageTk.PhotoImage(Image.open('images/frameicon.png'))
        tk.Label(master,image = self.systemlogo).pack(anchor= tk.W)
        
        #Creating admin tab
        self.addrectab = tk.Frame(master,bg ='#baced7',highlightbackground='white', highlightthickness = 2)
        self.addrectab.pack(fill='x')
        tk.Label(self.addrectab,text='Add Recipe   ',font=('Calibri',18),bg='#baced7').pack(side= tk.LEFT)
        tk.Button(self.addrectab,text= 'Exit',font= ("Calibri",18),background = '#baced7',width= 15, height= 1,borderwidth= 0, command=lambda: change_window(master, "from_addrec")).pack(side=tk.RIGHT)
        
        #Creating Addrec frame
        self.addrecframe = tk.Frame(master)
        self.addrecframe.pack(fill= 'both')
        
        # Adding Recipe labels
        tk.Label(self.addrecframe,text= 'Recipe Meal Type:',font= ("Calibri",18)).grid(column=0,row=0,sticky=tk.E,padx=5,pady=3)
        tk.Label(self.addrecframe,text='Recipe Name:',font= ("Calibri",18)).grid(column=0,row=1,sticky=tk.E,padx=5,pady=40)
        tk.Label(self.addrecframe,text= 'Recipe Ingredients:',font= ("Calibri",18)).grid(column=0,row=2,sticky=tk.E,padx=5)
        tk.Label(self.addrecframe,text= 'Recipe Procedure:',font= ("Calibri",18)).grid(column=0,row=3,sticky=tk.E,padx=5,pady=40)
        tk.Label(self.addrecframe,text= 'Recipe Price:',font= ("Calibri",18)).grid(column=0,row=4,sticky=tk.E,padx=5)
        tk.Label(self.addrecframe,text= 'Recipe Cooking time:',font= ("Calibri",18)).grid(column=0,row=5,sticky=tk.E,padx=5)
        
        
        # Adding Recipe Entries
        self.rectype = tk.Entry(self.addrecframe, width = 50)
        self.rectype.grid(column =1,row=0,sticky=tk.W,padx=5,pady=3,ipady=5)  
        self.recname = tk.Entry(self.addrecframe, width = 50)
        self.recname.grid(column =1,row=1,sticky=tk.W,padx=5,pady=40,ipady=5)
        self.recingr = tk.Entry(self.addrecframe, width = 50)
        self.recingr.grid(column =1,row=2,sticky=tk.W,padx=5,ipady=5)
        self.recpro = tk.Entry(self.addrecframe, width = 50)
        self.recpro.grid(column =1,row=3,sticky=tk.W,padx=5,pady=40,ipady=5)
        self.recprice = tk.Entry(self.addrecframe, width = 50)
        self.recprice.grid(column =1,row=4,sticky=tk.W,padx=5,ipady=5)
        self.rectime = tk.Entry(self.addrecframe, width = 50)
        self.rectime.grid(column =1,row=5,sticky=tk.W,padx=5,pady=40,ipady=5)
    
        #Creating Submit button
        self.submitbtn = tk.Button(self.addrecframe,text= 'Submit',font= ("Calibri",18),width= 15, height= 1,borderwidth= 1,background = '#ea6527', command =lambda: (reqRecipe(self.recname.get(), self.recingr.get(), self.recpro.get(), self.recprice.get(), self.rectime.get(), self.rectype.get())) (clear_text(self.recname,self.recingr,self.recpro,self.recprice,self.rectime,self.rectype)))
        self.submitbtn.grid(column=0,row=6, pady = 15,padx=10,sticky=tk.E)
        
        self.clrbtn = tk.Button(self.addrecframe, text="Clear", font= ("Calibri",18),width= 15, height= 1,borderwidth= 1,background = '#ea6527',command= lambda: clear_text(self.recname,self.recingr,self.recpro,self.recprice,self.rectime,self.rectype))
        self.clrbtn.grid(column=1, row=6, pady =15,padx=20,sticky=tk.W)
        
        self.addrecframe.columnconfigure(0,weight=1)
        self.addrecframe.columnconfigure(1,weight=1)
         

class AdminPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        
        master.title("Admin Page")
        master.geometry('1360x690+0+0')
        master.configure(bg='#ea6527')
        master.iconbitmap('icons/systemicon.ico')
        
        self.systemlogo = ImageTk.PhotoImage(Image.open('images/frameicon.png'))
        tk.Label(master,image = self.systemlogo).pack(anchor= tk.W)
        
        #Creating admin tab
        self.admintab = tk.Frame(master,bg ='#baced7',highlightbackground='white', highlightthickness = 2)
        self.admintab.pack(fill='x')
        tk.Label(self.admintab,text='Admin page   ',font=('Calibri',18),bg='#baced7').pack(side= tk.LEFT)
        tk.Button(self.admintab,text= 'Add Recipe',font= ("Calibri",18),background = '#baced7',width= 15, height= 1,borderwidth= 0, command=lambda: change_window(master, "AddRecipePage")).pack(side=tk.LEFT)
        tk.Button(self.admintab,text= 'Logout',font= ("Calibri",18),background = '#baced7',width= 15, height= 1,borderwidth= 0, command=lambda: logout(master)).pack(side=tk.RIGHT)

        #Creating admin frame
        self.adminframe = tk.Frame(master)
        self.adminframe.pack(fill='both')

        #Creating Recipe section (Left)
        self.adminlframe = tk.Frame(self.adminframe)
        self.adminlframe.grid(row=0, column=0)
        tk.Label(self.adminlframe,text='Active Recipe List',font=('Calibri',18)).pack()
        self.recipelist = tk.Listbox(self.adminlframe, width=50, height=25)
        self.recipelist.pack()
        conn = sqlite3.connect('DB.db')
        c = conn.cursor()

        c.execute("select * from Recipe where status = 'approved'")
        infox = c.fetchall()
        counterx = 0
        for recipeinfox in infox:
            self.recipelist.insert(counterx, recipeinfox[1])
            counterx += 1
        conn.close()
        

        tk.Button(self.adminlframe,text='Delete',font=('Calibri',18),background = '#ea6527', width=10, command = lambda: deleted(self.recipelist.get(ANCHOR), master)).pack(pady=45)

        #Creating Separator
        self.separator = ttk.Separator(self.adminframe, orient='vertical')
        self.separator.grid(row=0, column=1, sticky=(tk.S,tk.N))

        #Creating Recipe section (Right)
        self.adminrframe = tk.Frame(self.adminframe)
        self.adminrframe.grid(row=0, column=2)
        tk.Label(self.adminrframe,text='Pending Recipe List',font=('Calibri',18)).pack()
        self.suggestionlist = tk.Listbox(self.adminrframe, width=50, height=25)
        
        conn = sqlite3.connect('DB.db')
        c = conn.cursor()

        c.execute("select * from Recipe where status = 'pending'")
        info = c.fetchall()
        counter = 0
        for recipeinfo in info:
            self.suggestionlist.insert(counter, recipeinfo[1])
            counter += 1
        conn.close()

        self.suggestionlist.pack()
        tk.Button(self.adminrframe,text='View',font=('Calibri',18),background = '#ea6527', width=10, command = lambda: self.view_pending(self.suggestionlist.get(ANCHOR), master)).pack(pady=45)

        self.adminframe.columnconfigure(0, weight=1)
        self.adminframe.columnconfigure(1, weight=1)
        self.adminframe.columnconfigure(2, weight=1)
    
    def view_pending(self, selected, root):
        root.withdraw()
        master = tk.Toplevel()
        master.geometry("542x300")
        master.title(selected)
        master.iconbitmap('icons/systemicon.ico')
        print(selected)
        conn = sqlite3.connect('DB.db')
        c = conn.cursor()

        c.execute("select * from Recipe where status = 'pending' and recipe_name = :name",{
        'name' : selected  
        })

        info = c.fetchall()
            
        ingredients = "" 
        ingredients = info[0][2].replace("*","\n") 
        procedure = "" 
        procedure = info[0][3].replace("*","\n")

        self.name = selected
        self.recingre = ingredients
        self.recpro = procedure
        self.recprice = info[0][4]
        self.recitime = info[0][5]
        self.recmealtype = info[0][6]
        
        conn.commit()
        conn.close()

        #Creating scrollbar for recipes
        self.wrapper1 = tk.Frame(master)
        self.wrapper1.pack(fill="both", expand="yes")

        self.mycanvas = tk.Canvas(self.wrapper1)
        self.mycanvas.pack(side=tk.LEFT, fill="both", expand="yes")

        self.yscrollbar = ttk.Scrollbar(self.wrapper1, orient="vertical", command=self.mycanvas.yview)
        self.yscrollbar.pack(side=tk.RIGHT, fill="y")

        self.mycanvas.configure(yscrollcommand=self.yscrollbar.set)
        self.mycanvas.bind('<Configure>', lambda e: self.mycanvas.configure(scrollregion = self.mycanvas.bbox("all")))
        
        self.recFrame = tk.Frame(self.mycanvas)
        self.mycanvas.create_window((0,0), window=self.recFrame, anchor=tk.N)
        
        self.recname = tk.LabelFrame(self.recFrame, text="Recipe Name",font=('Calibri',18))
        self.recname.pack(pady=25)
        tk.Label(self.recname,text=selected,font=('Calibri',15)).pack()
        
        
        
        self.recingr = tk.LabelFrame(self.recFrame, text="Recipe Ingredients",font=('Calibri',18))
        self.recingr.pack()
        tk.Label(self.recingr,text=self.recingre,font=('Calibri',15)).pack()
        
        self.recproc = tk.LabelFrame(self.recFrame, text="Recipe Procedure",font=('Calibri',18))
        self.recproc.pack(pady=25)
        tk.Label(self.recproc,text=self.recpro,font=('Calibri',15)).pack()
        
        self.recpric = tk.LabelFrame(self.recFrame, text="Recipe Price",font=('Calibri',18))
        self.recpric.pack()
        tk.Label(self.recpric,text=self.recprice,font=('Calibri',15)).pack()
        
        self.rectime = tk.LabelFrame(self.recFrame, text="Recipe Time",font=('Calibri',18))
        self.rectime.pack(pady=25)
        tk.Label(self.rectime,text=self.recitime,font=('Calibri',15)).pack()
        
        self.rectype = tk.LabelFrame(self.recFrame, text="Recipe Meal Type",font=('Calibri',18))
        self.rectype.pack()
        tk.Label(self.rectype,text=self.recmealtype,font=('Calibri',15)).pack()
        
        self.recButton = tk.Frame(self.recFrame)
        self.recButton.pack(pady=25)
        tk.Button(self.recButton,text='Upload Image',font=('Calibri',18),background = '#ea6527',width=12, command = lambda: addImage(selected)).grid(column=0,row=0,padx=10)
        tk.Button(self.recButton,text='Okay',font=('Calibri',18),background = '#ea6527',width=12, command = lambda: approve(self.suggestionlist.get(ANCHOR), master)).grid(column=1,row=0,padx=10)
        tk.Button(self.recButton,text='Delete',font=('Calibri',18),background = '#ea6527',width=12, command = lambda: denied(self.suggestionlist.get(ANCHOR), master)).grid(column=2,row=0,padx=10)

def addImage(selected):
    file = filedialog.askopenfilename(initialdir = "images/",title = "Select image",filetypes = (("all files","*.png*"),("file_type","*.extension")))
    with open(file,'rb') as pic:
        picture = pic.read()
    
    conn = sqlite3.connect('DB.db')
    c = conn.cursor()

    c.execute("update Recipe set image = :pic where recipe_name = :name",{
    'name' : selected,
    'pic' : picture  
    })
    conn.commit()
    conn.close()
      



def approve(selected, master):
    conn = sqlite3.connect('DB.db')
    c = conn.cursor()

    c.execute("update Recipe set status = 'approved' where Recipe_name = :name",{
        'name' : selected  
    })
    c.execute("select recipe_id from recipe where recipe_name = :name",{
        'name' : selected
    })
    info = c.fetchall()
    c.execute("update recipe_request set recipe_status = 'approved' where Recipe_id = :name",{
        'name' : info[0][0]  
    })
    conn.commit()
    change_window(master, "AdminPage")
    conn.close()
        
def denied(selected, master):
    conn = sqlite3.connect('DB.db')
    c = conn.cursor()

    c.execute("update Recipe set status = 'denied' where Recipe_name = :name",{
        'name' : selected  
    })
    c.execute("select recipe_id from recipe where recipe_name = :name",{
        'name' : selected
    })
    info = c.fetchall()
    c.execute("update recipe_request set recipe_status = 'denied' where Recipe_id = :name",{
        'name' : info[0][0]  
    })
    conn.commit()
    change_window(master, "AdminPage")
    conn.close()

def deleted(selected, master):
    conn = sqlite3.connect('DB.db')
    c = conn.cursor()

    c.execute("update Recipe set status = 'deleted' where Recipe_name = :name",{
        'name' : selected  
    })
    c.execute("select recipe_id from recipe where recipe_name = :name",{
        'name' : selected
    })
    info = c.fetchall()
    c.execute("update recipe_request set recipe_status = 'deleted' where Recipe_id = :name",{
        'name' : info[0][0]  
    })
    conn.commit()
    change_window(master, "AdminPage")
    conn.close()

if __name__ == '__main__':
    main()