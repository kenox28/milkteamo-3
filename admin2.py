from tkinter import ttk
from tkinter import *
import mysql.connector
from tkinter.ttk import Treeview
from tkinter import messagebox
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
import os


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="milktea_shop"
)
mycursor = mydb.cursor()

milktea_tree = None  # Define milktea_tree as a global variable




def delete_image(flavor):
    try:
        image_path = f"images/{flavor}.png"
        if os.path.exists(image_path):
            os.remove(image_path)
    except FileNotFoundError:
        messagebox.showerror("Image Error", "Image file not found.")

def open_admin_window():
    admin_window = Tk()
    admin_window.title("Administrator Window")
    admin_window.geometry('700x400')
    admin_window.config(bg="#FFEBCD")



    admin=Label(admin_window,text='ADMINISTRATOR',font=('cooper black',20),bg="#FFEBCD")
    admin.place(x=80,y=20)



    def on_entry_click(e):
        if username_entry.get() == "Username:":
            username_entry.delete(0, "end")

    def on_entry_leave(e):
        if username_entry.get() == "":
            username_entry.insert(0, "Username:")

    username_entry = tk.Entry(admin_window, width=35, border=0, bg='#FFEBCD', font=('cooper black', 12))
    username_entry.place(x=50, y=150)
    username_entry.insert(0, "Username:")
    username_entry.bind('<FocusIn>', on_entry_click)
    username_entry.bind('<FocusOut>', on_entry_leave)
    Frame(admin_window, width=320, height=2, bg='black').place(x=50, y=170)

    # Create a password label and entry box

    def on_entry_click(e):
        if password_entry.get() == "Password:":
            password_entry.delete(0, "end")
            password_entry.config(show="*")

    def on_entry_leave(e):
        if password_entry.get() == "":
            password_entry.config(show="")
            password_entry.insert(0, "Password:")

    password_entry = tk.Entry(admin_window, width=35, border=0, bg='#FFEBCD', font=('cooper black', 12))
    password_entry.place(x=50, y=190)
    password_entry.insert(0, "Password:")
    password_entry.bind('<FocusIn>', on_entry_click)
    password_entry.bind('<FocusOut>', on_entry_leave)
    Frame(admin_window, width=320, height=2, bg='black').place(x=50, y=210)

    def login():
        # Check if the username and password are valid
        if username_entry.get() == "admin" and password_entry.get() == "w":
            admin_window.destroy()
            open_milkteas_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    log_in_button = tk.Button(admin_window, padx=70, text='LOGIN', bg='black', fg='white', border=3,
                              font=('cooper black', 11), command=login)
    log_in_button.place(x=100, y=270)

    admin_window.mainloop()

def open_milkteas_window():
    global milktea_tree  # Declare milktea_tree as a global variable
    global records_tree  # Declare records_tree as a global variable






    milkteas_window = Tk()
    milkteas_window.title("Milk Teas")
    milkteas_window.geometry('1400x800')

    milkteas_window.config(bg='#FFEBCD')

    order_lbl = Label(milkteas_window, text='Administrator Window', font=("cooper black", 17), bg='black', fg='white')
    order_lbl.place(x=0, y=5, width='1400', height=40)

    back_lbl = Button(milkteas_window, text="LOG OUT", bg="black", fg="white", bd=0,
                      font=("cooper black", 15), command=milkteas_window.destroy)
    back_lbl.place(x=1250, y=60)

    frm = Frame(milkteas_window, bg='#8B7D6B')
    frm.place(x=50, y=90, width=1400, height=550)

    milktea_lbl = Label(frm, text='Milk Tea Name:', font=("cooper black", 14), bg='black', fg='white')
    milktea_lbl.place(x=50, y=50)

    price_lbl = Label(frm, text='Price:', font=("cooper black", 14), bg='black', fg='white')
    price_lbl.place(x=50, y=100)

    info_lbl = Label(frm, text='Information:', font=("cooper black", 14), bg='black', fg='white')
    info_lbl.place(x=50, y=150)

    stocks_lbl = Label(frm, text='Stocks:', font=("cooper black", 14), bg='black', fg='white')
    stocks_lbl.place(x=50, y=200)

    milktea_entry = Entry(frm, font=("cooper black", 14), width=20)
    milktea_entry.place(x=50, y=80)

    price_entry = Entry(frm, font=("cooper black", 14), width=20)
    price_entry.place(x=50, y=130)

    info_entry = Entry(frm, font=("cooper black", 14), width=20)
    info_entry.place(x=50, y=180)

    stocks_entry = Entry(frm, font=("cooper black", 14), width=20)
    stocks_entry.place(x=50, y=230)



    def add_milk_tea_flavor():
        flavor = milktea_entry.get()
        price = price_entry.get()
        information = info_entry.get()
        stocks = stocks_entry.get()

        if flavor and price and information and stocks:
            # Insert the new milk tea flavor into the database
            sql = "INSERT INTO milktea2 (flavor, price, information, stocks) VALUES (%s, %s, %s, %s)"
            val = (flavor, price, information, stocks)
            mycursor.execute(sql, val)
            mydb.commit()

            messagebox.showinfo("Success", "Flavor added successfully!")

            # Upload the image for the new milk tea flavor
            image_path = filedialog.askopenfilename(title="Select Image",
                                                    filetypes=(("Image files", "*.png *.jpg *.jpeg"),))
            if image_path:
                upload_image(flavor, image_path)

            # Update the milktea_tree with the new flavor
            milktea_tree.insert("", "end", values=(flavor, price, information, stocks))
        else:
            messagebox.showerror("Error", "Please enter a flavor name, price, information, and stocks.")

    def upload_image(flavor, image_path):
        try:
            # Create the 'images' directory if it doesn't exist
            if not os.path.exists("images"):
                os.makedirs("images")

            # Open the image file
            image = Image.open(image_path)

            # Resize the image as needed
            image = image.resize((100, 100))

            # Save the resized image
            image.save(f"images/{flavor}.png")
        except FileNotFoundError:
            messagebox.showerror("Image Error", "Image file not found.")

    def delete_milk_tea():
        selected_item = milktea_tree.selection()
        if not selected_item:
            messagebox.showwarning("Delete Error", "Please select a milk tea flavor to delete.")
            return

        flavor = milktea_tree.item(selected_item, "values")[0]
        delete_image(flavor)

        # Delete the milk tea flavor from the database
        sql = "DELETE FROM milktea2 WHERE flavor = %s"
        val = (flavor,)
        mycursor.execute(sql, val)
        mydb.commit()

        # Remove the milk tea flavor from the Treeview
        milktea_tree.delete(selected_item)

        messagebox.showinfo("Success", "Flavor deleted successfully!")

    def delete_image(flavor):
        # Delete the corresponding image file if it exists
        image_path = f"images/{flavor}.png"
        if os.path.exists(image_path):
            os.remove(image_path)

    def delete_record():
        selected_item = records_tree.selection()
        if not selected_item:
            messagebox.showwarning("Delete Error", "Please select a record to delete.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected record?")
        if confirm:
            # Delete the record from the database
            records_tree.delete(selected_item)
            messagebox.showinfo("Success", "Record deleted successfully!")

    def calculate_total():
        total = 0
        for child in records_tree.get_children():
            total += float(records_tree.item(child, "values")[1])

        messagebox.showinfo("Total", f"The total amount is: {total}")

    def delete_all_records():
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all records?")
        if confirm:
            # Delete all records from the database
            mycursor.execute("DELETE FROM purchases")
            mydb.commit()

            # Delete all columns in the Treeview
            records_tree.delete(*records_tree.get_children())

            messagebox.showinfo("Success", "All records deleted successfully!")

    def update_milk_tea():
        selected_item = milktea_tree.selection()
        if not selected_item:
            messagebox.showwarning("Update Error", "Please select a milk tea flavor to update.")
            return

        flavor = milktea_tree.item(selected_item, "values")[0]
        new_price = price_entry.get()
        new_information = info_entry.get()
        new_stocks = stocks_entry.get()

        if new_price and new_information and new_stocks:
            # Update the milk tea flavor in the database
            sql = "UPDATE milktea2 SET price = %s, information = %s, stocks = %s WHERE flavor = %s"
            val = (new_price, new_information, new_stocks, flavor)
            mycursor.execute(sql, val)
            mydb.commit()

            messagebox.showinfo("Success", "Flavor updated successfully!")

            # Update the values in the milktea_treeview
            milktea_tree.set(selected_item, "price", new_price)
            milktea_tree.set(selected_item, "information", new_information)
            milktea_tree.set(selected_item, "stocks", new_stocks)
        else:
            messagebox.showerror("Error", "Please enter a new price, information, and stocks.")

    def open_messages():
        def on_message_select(event):
            selected_item = messages_tree.focus()
            selected_message = messages_tree.item(selected_item)["values"][0]
            messages_text.delete(1.0, "end")
            messages_text.insert("end", selected_message)

        def on_message_double_click(event):
            selected_item = messages_tree.focus()
            selected_message = messages_tree.item(selected_item)["values"][0]
            messages_text.delete(1.0, "end")
            messages_text.insert("end", selected_message)
            messages_text.see("end")

        messages_window = Tk()
        messages_window.title("Messages")
        messages_window.geometry('800x400')

        messages_window.config(bg='#FFEBCD')


        messages_lbl = Label(messages_window, text='Report Messages', font=("cooper black", 17), bg='black', fg='white')
        messages_lbl.place(x=0, y=5, width='800', height=40)

        messages_text = Text(messages_window, font=("cooper black", 14), width=30, height=10, wrap='word')
        messages_text.place(x=50, y=60)

        # Create the Treeview to display the messages
        messages_tree = ttk.Treeview(messages_window, columns=("messages", "date_added"), show="headings")
        messages_tree.place(x=50, y=60, width=700)

        messages_tree.column("messages", anchor="w", width=500)  # Adjust the width as needed
        messages_tree.heading("messages", text="Messages")

        messages_tree.column("date_added", anchor="w", width=150)
        messages_tree.heading("date_added", text="Date Added")

        # Retrieve the messages from the database
        mycursor.execute("SELECT messages, date_added FROM report")
        messages = mycursor.fetchall()

        for message in messages:
            messages_tree.insert("", "end", values=(message[0], message[1]))

        messages_tree.bind("<<TreeviewSelect>>", on_message_select)
        messages_tree.bind("<Double-1>", on_message_double_click)

        messages_text.configure(state='disabled')



    # Add an "Update Milk Tea" button and connect it to the update_milk_tea function

    update_milktea_btn = Button(frm, text='Update Milk Tea', font=("cooper black", 14), bg='black', fg='white',
                                command=update_milk_tea)
    update_milktea_btn.place(x=380, y=500)

    reportbutton = Button(frm, text="OPEN MESSAGES", padx=90, border=6,bg="black", fg="white", font=('cooper black', 15),
                          command=open_messages)
    reportbutton.place(x=850, y=130)

    milktea_btn = Button(frm,padx=12, text='Add Milk Tea', font=("cooper black", 14),bg='black',fg='white', command=add_milk_tea_flavor)
    milktea_btn.place(x=50, y=500)

    delete_milktea_btn = Button(frm, text='Delete Milk Tea', font=("cooper black", 14),bg='black',fg='white', command=delete_milk_tea)
    delete_milktea_btn.place(x=210, y=500)

    delete_record_btn = Button(frm, text='Delete Record', font=("cooper black", 14),bg='black',fg='white', command=delete_record)
    delete_record_btn.place(x=700, y=500)

    calculate_total_btn = Button(frm, text='Total', font=("cooper black", 14),bg='black',fg='white', command=calculate_total)
    calculate_total_btn.place(x=1000, y=500)

    delete_all_btn = Button(frm, text='Delete All', font=("cooper black", 14), bg='black', fg='white',
                            command=delete_all_records)
    delete_all_btn.place(x=1180, y=500)
    # Create the Treeview to display the milk tea flavors
    milktea_tree = Treeview(frm, columns=("flavor", "price", "information", "stocks"), show="headings",
                            selectmode="browse")
    milktea_tree.place(x=50, y=270)

    # Add column headings
    milktea_tree.column("#0", width=0, stretch=NO)
    milktea_tree.column("flavor", anchor=W, width=150)
    milktea_tree.column("price", anchor=W, width=100)
    milktea_tree.column("information", anchor=W, width=200)
    milktea_tree.column("stocks", anchor=W, width=50)

    milktea_tree.heading("#0", text="", anchor=W)
    milktea_tree.heading("flavor", text="Milk Tea Flavor", anchor=W)
    milktea_tree.heading("price", text="Price", anchor=W)
    milktea_tree.heading("information", text="Information", anchor=W)
    milktea_tree.heading("stocks", text="Stocks", anchor=W)

    # Retrieve the milk tea flavors from the database
    mycursor.execute("SELECT flavor, price, information, stocks FROM milktea2")
    flavors = mycursor.fetchall()

    # Populate the Treeview with the milk tea flavors
    for flavor, price, information, stocks in flavors:
        milktea_tree.insert("", "end", values=(flavor, price, information, stocks))

    # Create the Treeview for the purchase records
    records_tree = Treeview(frm, columns=("customer_name", "total_amount", "date_added"), show="headings", selectmode="browse")
    records_tree.place(x=700, y=270)

    # Add column headings for the purchase records
    records_tree.heading("customer_name", text="Customer Name")
    records_tree.heading("total_amount", text="Total Amount")
    records_tree.heading("date_added", text="Date Added")  # Add this line

    # Retrieve the purchase records from the database
    mycursor.execute("SELECT customer_name, total_amount ,date_added FROM purchases")
    records = mycursor.fetchall()

    # Populate the Treeview with the purchase records
    for customer_name, total_amount, date_added in records:
        records_tree.insert("", "end", values=(customer_name, total_amount, date_added))

    def generate_sales_report_graph():
        milkteas_window.destroy()
        import Report
        Report.generate_sales_report_graph()

    sales_button = Button(milkteas_window,text="SALES REPORT", padx=100, border=6, bg="black", fg="white",
                          font=('cooper black', 15), command=generate_sales_report_graph)
    sales_button.place(x=900, y=130)






    milkteas_window.mainloop()






# Open the admin window
open_admin_window()
