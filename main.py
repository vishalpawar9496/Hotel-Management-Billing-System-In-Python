from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tmsg
import os
import time
#=========================================Python Variables=====================================
menu_category = ["Tea & Coffee", "Beverages", "Fast Food", "South Indian", "Starters", "Main Course", "Dessert"]

menu_category_dict = {"Tea & Coffee":"1 Tea & Coffee.txt", "Beverages":"2 Beverages.txt", "Fast Food":"3 Fast Food.txt",
                    "South Indian":"4 South Indian.txt", "Starters":"5 Starters.txt", "Main Course":"6 Main Course.txt", "Dessert":"7 Dessert.txt"}


order_dict = {}
for i in menu_category:
    order_dict[i] = {}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

#=========================Backend Functions starts=====================================

#=============load menu function defining=============================

def load_menu():
    menuCategory.set("")
    menu_table.delete(*menu_table.get_children())
    menu_file_list = os.listdir("Menu")
    for file in menu_file_list:
        f = open("Menu\\" + file , "r")
        category = ""
        while True:
            line = f.readline()
            if(line==""):
                menu_table.insert('',END,values=["","",""])
                break
            elif(line=="\n"):
                continue
            elif(line[0]=='#'):
                category = line[1:-1]
                name = "\t\t" + line[:-1]
                price = ""
            else:
                name = line[:line.rfind(" ")]
                price = line[line.rfind(" ")+1:-3]
            menu_table.insert('',END,values=[name,price,category])

#=========================defining load order function====================================

def load_order():
    order_table.delete(*order_table.get_children())
    for category in order_dict.keys():
        if order_dict[category]:
            for lis in order_dict[category].values():
                order_table.insert('',END,values=lis)
    update_total_price()

#====================add button functioning================
def add_button():
    name = itemName.get()
    rate = itemRate.get()
    category = itemCategory.get()
    quantity = itemQuantity.get()

    if name in order_dict[category].keys():
        tmsg.showinfo("Error","Item  already exist in your order")
        return
    if not quantity.isdigit():
        tmsg.showinfo("Error","Please Enter valid Quantity")
        return
    lis = [name,rate,quantity, str(int(rate)*int(quantity)),category]
    order_dict[category][name] = lis
    load_order()

#===============================load item from menu to order container=================================

def load_item_from_menu(event):
    cursor_row = menu_table.focus()
    contents = menu_table.item(cursor_row)
    row = contents["values"]

    itemName.set(row[0])
    itemRate.set(row[1])
    itemCategory.set(row[2])
    itemQuantity.set("1")

def load_item_from_order(event):
    cursor_row = order_table.focus()
    contents = order_table.item(cursor_row)
    row = contents["values"]

    itemName.set(row[0])
    itemRate.set(row[1])
    itemQuantity.set(row[2])
    itemCategory.set(row[4])

def show_button_operation():
    category = menuCategory.get()
    if category not in  menu_category:
        tmsg.showinfo("Error","Please select valid Choice")
    else:
        menu_table.delete(*menu_table.get_children())
        f = open("Menu\\" + menu_category_dict[category] , "r")
        while True:
            line = f.readline()
            if(line==""):
                break
            if(line[0]=='#' or line=="\n"):
                continue
            if(line[0]=='*'):
                name = "\t"+ line[:-1]
                menu_table.insert('',END, values=[name,"",""])
            else:
                name = line[:line.rfind(" ")]
                price = line[line.rfind(" ") +1:-3]
                menu_table.insert('',END,values=[name,price,category])

#==================clear the contents in conatiner==================================

def clear_button_operation():
    itemName.set("")
    itemRate.set("")
    itemQuantity.set("")
    itemCategory.set("")

def cancel_button_operation():
    names = []
    for i in menu_category:
        names.extend(list(order_dict[i].keys()))
    if len(names)==0:
        tmsg.showinfo("Error","Your order list is Empty")
        return
    ans = tmsg.showinfo("Cancel order","Are you sure you want to cancel the order ?")
    if ans=="no":
        return
    order_table.delete(*order_table.get_children())
    for i in  menu_category:
        order_dict[i] = {}
    clear_button_operation()
    update_total_price()

def update_button_operation():
    name = itemName.get()
    rate = itemRate.get()
    category = itemCategory.get()
    quantity = itemQuantity.get()

    if category==" ":
        return
    if name not in order_dict[category].keys():
        tmsg.showinfo("Error","No  changes in Quantity")
        return
    order_dict[category][name][2] = quantity
    order_dict[category][name][3] = str(int(rate)*int(quantity))
    load_order()

def remove_button_operation():
    name = itemName.get()
    category = itemCategory.get()

    if category=="":
        return
    if name not in order_dict[category].keys():
        tmsg.showinfo("Error","Item is not in your order list")
        return
    del order_dict[category][name]
    load_order()

def update_total_price():
    price = 0
    for i in menu_category:
        for j in order_dict[i].keys():
            price += int(order_dict[i][j][3])
    if price == 0:
        totalPrice.set("")
    else:
        totalPrice.set("Rs. "+str(price)+"  /-")

def bill_button_operation():
    customer_name = customerName.get()
    customer_contact = customerContact.get()
    names = []
    for i in menu_category:
        names.extend(list(order_dict[i].keys()))
    if len(names)==0:
        tmsg.showinfo("Error","Your order list is Empty")
        return
    if customer_name=="" or customer_contact=="":
        tmsg.showinfo("Error","Customer Details Required")
        return
    if not customerContact.get().isdigit():
        tmsg.showinfo("Error","Invalid Customer Contact")
        return
    ans = tmsg.askquestion("Generate Bill"," Are You Sure You Want To Generate Bill ?")
    ans = "yes"
    if ans=="yes":
        bill = Toplevel()
        bill.title("Bill")
        bill.geometry("670x500+300+100")
        bill.wm_iconbitmap("Coffee.ico")
        bill_text_area = Text(bill, font=("arial",13))
        st = "\t\t\tVishal's Restaurant\n\t\tVishal Pawar,NH-56 Nashik Road Aurangabad-431001\n"
        st += "\t\t\tGST.No:- 99AGDGG9969GIFH\n"
        st += "-"*61 + "BILL" + "-"*61 + "\nDate:-"
#===================Date And Time=======================================
        t = time.localtime(time.time())
        week_day_dict = {0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"}
        st += f"{t.tm_mday} / {t.tm_mon} / {t.tm_year} ({week_day_dict[t.tm_wday]})"
        st += " "*10 + f"\t\t\t\t\t\tTime:- {t.tm_hour} : {t.tm_min} : {t.tm_sec}"

#=====================customer NAME AND CONTACT==========================
        st += f"\nCustomer Name:- {customer_name}\nCustomer Contact:- {customer_contact}\n"
        st += "-"*130 + "\n" + " "*4 + "DESCRIPTION\t\t\t\t\tRate\tQUANTITY\t\tAMOUNT\n"
        st += "-"*130 + "\n"

#====================LIST OF ITEMS==============================
        for i in menu_category:
            for j in order_dict[i].keys():
                lis = order_dict[i][j]
                name = lis[0]
                rate = lis[1]
                quantity = lis[2]
                price = lis[3]
                st += name + "\t\t\t\t\t" + rate + "\t     " + quantity + "\t\t  " + price + "\n\n"
        st += "-"*130

#========================Total price==============================
        st += f"\n\t\t\tTotal price : {totalPrice.get()}\n"
        st += "-"*130

#===============display bill  in new window======================================
        bill_text_area.insert(1.0, st)

#=====================write into file=========================
        folder = f"{t.tm_mday},{t.tm_mon},{t.tm_year}"
        if not os.path.exists(f"Bill Records\\{folder}"):
            os.makedirs(f"Bill Records\\{folder}")
        file = open(f"Bill Records\\{folder}\\{customer_name+customer_contact}.txt", "w")
        file.write(st)
        file.close()

#======================Clear Operations====================
        order_table.delete(*order_table.get_children())
        for i in menu_category:
            order_dict[i] = {}
        clear_button_operation()
        update_total_price()
        customerName.set("")
        customerContact.set("")

        bill_text_area.pack(expand=True, fill=BOTH)
        bill.focus_set()
        bill.protocol("WM_DELETE_WINDOW",close_window)

def close_window():
    tmsg.showinfo("Thanks","Thanks for using our service")
    root.destroy()






#================Tk root for Front END===================
root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w,h))
root.title("Welcome To Vishal Restaurant  || Developed By Vishal Pawar")
root.wm_iconbitmap("Burger.ico")

#===============Title====================
style_button = ttk.Style()
style_button.configure('TButton',font=('arial',12,'bold'),bg='lightgreen')


title_frame = Frame(root,bd=8,bg='orange',relief='raise')
title_frame.pack(side=TOP, fill="x")

title_label = Label(title_frame, text="Welcome To Vishal's Restaurant",bd=12,relief='raise', font=('arial',24,'bold'),bg='orange',pady=5)
title_label.pack()

#====================================Customer Details=======================
customer_frame = Label(root, text='Customer Details',font=('arial',16,'bold'),bd=8,bg='lightblue',relief='groove')
customer_frame.pack(side=TOP,fill="x")

customer_name = Label(customer_frame,text='Name:',font=('arial',15,'bold'),bg='lightgreen')
customer_name.grid(row=0, column=0)

customerName = StringVar()
customerName.set("")

customer_name_entry = Entry(customer_frame,width=20,font=('arial',15,'bold'),bd=5,textvariable=customerName)
customer_name_entry.grid(row=0, column=1,padx=50)


customer_contact_label = Label(customer_frame,text='Contact',font=('arial',16,'bold'),bg='lightgreen')
customer_contact_label.grid(row=0,column=2)

customerContact = StringVar()
customerContact.set("")

customer_contact_entry = Entry(customer_frame,width=20,font=('arial',16,'bold'),bd=5,textvariable=customerContact)
customer_contact_entry.grid(row=0,column=3,padx=50)


#===========================Menu============================================
menu_frame = Frame(root,bd=10,bg='lightblue',relief='groove')
menu_frame.place(x=0,y=125,height=595,width=680)

menu_label = Label(menu_frame,text="Menu",font=('arial',20,'bold'),bg='lightblue',bd=15,relief='raise',pady=0)
menu_label.pack(side=TOP,fill="x")

menu_category_frame = Frame(menu_frame,bg='lightblue',pady=10)
menu_category_frame.pack(fill="x")

combo_label = Label(menu_category_frame,text='Select Type',font=('arial',16,'bold'),bg='lightgreen',relief='ridge',bd=3)
combo_label.grid(row=0,column=0,padx=10)

menuCategory = StringVar()
combo_menu = ttk.Combobox(menu_category_frame,values=menu_category, textvariable=menuCategory)
combo_menu.grid(row=0,column=1,padx=30)


show_button = Button(menu_category_frame,text="Show",width=10,font=("arial 10 bold"),command=show_button_operation)
show_button.grid(row=0,column=2,padx=40)

showall_button = Button(menu_category_frame,text="Show All",width=10,font=("arial 10 bold"),command=load_menu)
showall_button.grid(row=0,column=3,padx=5)

#====================================Menu TreeView====================================
menu_table_frame = Label(menu_frame)
menu_table_frame.pack(fill=BOTH,expand=1)

scrollbar_menu_x =Scrollbar(menu_table_frame,orient=HORIZONTAL)
scrollbar_menu_y = Scrollbar(menu_table_frame,orient=VERTICAL)

style = ttk.Style()
style.configure("TreeView.Heading",font=('arial',15,'bold'))
style.configure("Treeview",font=('arial',13,'bold'),rowheight=25)

menu_table = ttk.Treeview(menu_table_frame,style='Treeview',columns=("name","price","category"),xscrollcommand=scrollbar_menu_x.set,
            yscrollcommand=scrollbar_menu_y.set)
menu_table.heading("name",text="Name")
menu_table.heading("price",text="Price")
menu_table["displaycolumns"]=("name","price")
menu_table["show"] = "headings"
menu_table.column("price",width=50,anchor='center')

scrollbar_menu_x.pack(side=BOTTOM,fill=X)
scrollbar_menu_y.pack(side=RIGHT,fill=Y)

scrollbar_menu_x.configure(command=menu_table.xview)
scrollbar_menu_y.configure(command=menu_table.yview)
menu_table.pack(fill=BOTH,expand=1)

load_menu()
menu_table.bind("<ButtonRelease-1>", load_item_from_menu)

####################################################################################################

#======================================Second Panel for Items creation=====================================
item_frame = Frame(root, bd=8, bg='lightblue',relief='groove')
item_frame.place(x=680,y=125, height=230,width=680)

item_title_label = Label(item_frame, text='Item',font=('arial',20,'bold'),bg='lightblue',fg='#262626',bd=15,relief='raise')
item_title_label.pack(side=TOP,fill='x')

item_frame2 = Frame(item_frame,bg='lightblue')
item_frame2.pack(fill=X)

item_name_label = Label(item_frame2,text='Name:', font=("arial",13,'bold'),bg='lightgreen',relief='ridge',bd=4)
item_name_label.grid(row=0,column=0)
itemCategory = StringVar()
itemCategory.set("")
itemName = StringVar()
itemName.set("")
item_name = Entry(item_frame2, font=('arial',12,'bold'),state=DISABLED,width=25,textvariable=itemName,bd=4)
item_name.grid(row=0,column=1,padx=10)


item_rate_label = Label(item_frame2, text="Rate:", font=('arial',13,'bold'),bg='lightgreen',relief='ridge',bd=4)
item_rate_label.grid(row=0,column=2,padx=40)

itemRate = StringVar()
itemRate.set("")
item_rate = Entry(item_frame2, font=('arial',13,'bold'),bd=3,textvariable=itemRate, state=DISABLED, width=10)
item_rate.grid(row=0,column=3, padx=30, pady=15)


item_quantity_label = Label(item_frame2, text="Quantity", font=('arial',12,'bold'),bg='lightgreen',relief='ridge',bd=4)
item_quantity_label.grid(row=1,column=0,padx=30,pady=11)

itemQuantity = StringVar()
itemQuantity.set("")
item_quantity = Entry(item_frame2, font=('arial',13,'bold'),bd=3,width=20,textvariable=itemQuantity)
item_quantity.grid(row=1,column=1,padx=15)

#=====================Frame 3 For Buttons=======================
item_frame3 = Frame(item_frame,bg='lightblue')
item_frame3.pack(fill=X)

add_button = Button(item_frame3, text='Add Item',bd=3,font=('arial',9,'bold'),command=add_button)
add_button.grid(row=0,column=0,padx=40,pady=5)

remove_button = Button(item_frame3, text='Remove Item',bd=3,font=('arial',9,'bold'),command=remove_button_operation)
remove_button.grid(row=0,column=1,padx=40,pady=5)

update_button = Button(item_frame3,text='Update Quantity',bd=3,font=('arial',9,'bold'),command=update_button_operation)
update_button.grid(row=0,column=2,padx=40,pady=5)

clear_button = Button(item_frame3,text='Clear Panel',bd=3,font=('arial',9,'bold'),command=clear_button_operation)
clear_button.grid(row=0,column=3,padx=40,pady=5)

#==============================================Order Frame=============================
order_frame = Frame(root,bd=8,bg='lightblue',relief='groove')
order_frame.place(x=680,y=335,height=380,width=675)


order_frame_label = Label(order_frame, text="Your Order", font=('arial',20,'bold'),bg='lightgreen',relief='ridge',bd=4)
order_frame_label.pack(side=TOP,fill="x")

#========================================Order Table Content container===================================

order_table_frame = Frame(order_frame)
order_table_frame.place(x=0,y=40,height=265,width=670)

scrollbar_order_x = Scrollbar(order_table_frame,orient=HORIZONTAL)
scrollbar_order_y = Scrollbar(order_table_frame,orient=VERTICAL)

order_table = ttk.Treeview(order_table_frame, columns=("name","rate","quantity","price","category"),xscrollcommand=scrollbar_order_x.set,yscrollcommand=scrollbar_order_y.set)

order_table.heading("name",text="Name")
order_table.heading("rate",text="Rate")
order_table.heading("quantity",text="Quantity")
order_table.heading("price",text="Price")
order_table["displaycolumns"]=("name","rate","quantity","price")
order_table["show"] = "headings"
order_table.column("rate",width=100,anchor="center",stretch=NO)
order_table.column("quantity",width=100,anchor="center",stretch=NO)
order_table.column("price",width=100,anchor="center",stretch=NO)

order_table.bind("<ButtonRelease-1>",load_item_from_order)

scrollbar_order_x.pack(side=BOTTOM,fill=X)
scrollbar_order_y.pack(side=RIGHT,fill=Y)

scrollbar_order_x.configure(command=order_table.xview)
scrollbar_order_y.configure(command=order_table.yview)

order_table.pack(fill=BOTH,expand=1)

#============================================Item Order table Bottom Working==================================================

total_price_label = Label(order_frame,text='Total Price:',relief='ridge',bd=4, font=('arial',14,'bold'),bg='lightgreen')
total_price_label.pack(side=LEFT,anchor=SW,padx=20,pady=10)

totalPrice = StringVar()
totalPrice.set("")

total_price_entry = Entry(order_frame,width=10, font=('arial',13,'bold'),bd=4,textvariable=totalPrice,state=DISABLED)
total_price_entry.pack(side=LEFT,anchor=SW,padx=0,pady=10)

bill_button = Button(order_frame,text="BILL",bd=4,font=('arial',9,'bold'),width=11,command=bill_button_operation)
bill_button.pack(side=LEFT, anchor=SW, padx=35,pady=10)

cancel_button = Button(order_frame,text="Cancel Order",bd=4,font=('arial',9,'bold'),command=cancel_button_operation)
cancel_button.pack(side=RIGHT, anchor=SW, padx=20,pady=10)

root.mainloop()