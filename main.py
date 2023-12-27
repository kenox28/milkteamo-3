from tkinter import *
from PIL import ImageTk, Image
import mysql.connector
from tkinter import Text, Scrollbar
import tkinter.messagebox as messagebox


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="milktea_shop"
)
mycursor = mydb.cursor()


window = Tk()
window.title("MENU")
window.geometry('1330x750')
window.config(bg='white')



milktittle=Label(window,text="MILKTE'AMO❤",bg='black',fg='white',font=("cooper black",20))
milktittle.place(x=0, y=0, width=850, height=40)



def display_menu():
    menu_frame = Frame(bg="#FFEBCD")
    menu_frame.place(x=30, y=100, width=800, height=600) # Adjust the width and height of the menu frame

    lbl = Label(menu_frame, text='MENU', font=('cooper black', 25), fg='white', bg="black")
    lbl.place(x=0, y=0,width=800,height=25)
    Frame(menu_frame, width=820, height=4, bg='black').place(x=0, y=290)

    # Configure the grid layout and column configuration of the menu frame
    menu_frame.grid_rowconfigure(0, weight=1)
    menu_frame.grid_rowconfigure(1, weight=1)
    menu_frame.grid_rowconfigure(2, weight=1)
    menu_frame.grid_rowconfigure(3, weight=1)
    menu_frame.grid_columnconfigure(0, weight=1)
    menu_frame.grid_columnconfigure(1, weight=1)
    menu_frame.grid_columnconfigure(2, weight=1)
    menu_frame.grid_columnconfigure(3, weight=1)

    cart_frame = Frame(bg="#FFEBCD")
    cart_frame.place(x=850, y=100, width=450, height=600)

    # Fetch milk tea flavors from the database
    mycursor.execute("SELECT flavor, price FROM milktea2")
    milktea_flavors = mycursor.fetchall()

    total_price = 0  # Initialize the total price variable
    chosen_flavors = []
    # Create a dictionary to store flavor prices
    flavor_price_dict = {}

    # Store flavor prices in the dictionary
    for flavor in milktea_flavors:
        flavor_name = flavor[0]
        flavor_price = flavor[1]
        flavor_price_dict[flavor_name] = flavor_price

    # Create a function to display flavor details in a new window
    from tkinter import DISABLED

    def open_flavor_window(flavor):
        flavor_window = Toplevel(window)
        flavor_window.title("Flavor Details - " + flavor)
        flavor_window.geometry('400x600')
        flavor_window.config(bg='#FFEBCD')

        def remove_from_cart():
            nonlocal total_price

            flavor_name = flavor_window.title().split(" - ")[1]
            flavor_price = flavor_price_dict[flavor_name]

            total_price -= flavor_price  # Update the total price

            # Remove the item from the cart frame
            for item in cart_frame.winfo_children():
                item_text = item["text"]
                if flavor_name in item_text:
                    item.destroy()

            total_price_label.config(text="Total Price: ₱" + str(total_price), bg="#FFEBCD", fg="black")

        remove_button = Button(flavor_window, text="Remove", font=('cooper black', 14), bg="#FFEBCD", fg="black",
                               command=remove_from_cart)
        remove_button.place(x=150, y=550)

        def add_to_cart(flavor_name, flavor_price):
            nonlocal total_price

            # Update the total price
            total_price += flavor_price

            # Append the flavor name to the chosen_flavors list
            chosen_flavors.append(flavor_name)

            # Create a cart item label for the chosen flavor
            cart_item_label = Label(cart_frame, text=flavor_name + " ₱" + str(flavor_price),
                                    font=('cooper black', 14), bg="#FFEBCD", fg="black")
            cart_item_label.place(x=10, y=len(cart_frame.winfo_children()) * 25)

            # Update the total price label
            total_price_label.config(text="Total Price: ₱" + str(total_price))

        # Consume the unread result from the previous query
        mycursor.fetchall()

        mycursor.execute("SELECT price, information FROM milktea2 WHERE flavor = %s", (flavor,))
        result = mycursor.fetchone()



        if result:
            price = result[0]
            information = result[1]

            flavor_label = Label(flavor_window, text="Milk Tea Name: " + flavor, font=('cooper black', 14),
                                 bg="#FFEBCD",
                                 fg="black")
            flavor_label.pack(pady=10)

            price_label = Label(flavor_window, text="Price: ₱" + str(price), font=('cooper black', 14), bg="#FFEBCD",
                                fg="black")
            price_label.pack(pady=10)

            information_text = Text(flavor_window, font=('cooper black', 14), bg="#FFEBCD", fg="black", height=10,
                                    wrap="word")
            information_text.pack(pady=10)

            scrollbar = Scrollbar(flavor_window, command=information_text.yview)
            scrollbar.pack(side="right", fill="y")
            information_text.configure(yscrollcommand=scrollbar.set)

            information_text.insert("1.0", "Information:\n" + information)
            information_text.configure(state=DISABLED)  # Disable editing of the text

            Addlist = Button(flavor_window, text="ADD TO LIST", font=('cooper black', 14), bg="#FFEBCD", fg="black",
                             command=lambda flavor_name=flavor, flavor_price=price: add_to_cart(flavor_name,
                                                                                                flavor_price))
            Addlist.place(x=150, y=500)
        else:
            error_label = Label(flavor_window, text="Flavor details not found.", font=('cooper black', 14))
            error_label.pack(pady=10)

        flavor_window.mainloop()

    # Display milk tea flavors as buttons in the menu frame
    row = 0
    column = 0
    button_padding = 20  # Adjust the padding around the buttons

    for flavor in milktea_flavors:
        flavor_name = flavor[0]
        flavor_image_path = f"images/{flavor_name}.png"  # Change the image file extension if necessary

        try:
            flavor_image = Image.open(flavor_image_path)
            # Calculate the new width based on the desired width (e.g., 200) while maintaining the aspect ratio
            width, height = flavor_image.size
            new_width = 200
            new_height = int((new_width / width) * height)
            flavor_image = flavor_image.resize((new_width, new_height))  # Resize the image
            flavor_button_image = ImageTk.PhotoImage(flavor_image)
            flavor_button = Button(menu_frame, image=flavor_button_image, text=flavor_name, compound="top",
                                   bg='black', fg='white', font=('cooper black', 14),
                                   command=lambda flavor=flavor_name: open_flavor_window(flavor))
            flavor_button.image = flavor_button_image  # Store a reference to prevent image garbage collection
            flavor_button.grid(row=row, column=column, padx=button_padding, pady=button_padding)
        except FileNotFoundError:
            flavor_button = Button(menu_frame, text=flavor_name, bg='black', fg='black', font=('cooper black', 14),
                                   command=lambda flavor=flavor_name: open_flavor_window(flavor))
            flavor_button.grid(row=row, column=column, padx=button_padding, pady=button_padding)

        column += 1
        if column == 4:
            column = 0
            row += 1
    carttitle = Label(cart_frame, text='milktea list', font=('cooper black', 30), fg='white', bg="black")
    carttitle.place(x=0, y=0, width=450, height=40)

    # Display the total price label and customer name entry in the cart frame
    total_price_label = Label(cart_frame, text="Total Price: ₱" + str(total_price), font=('cooper black', 14), bg="#FFEBCD", fg="black")
    total_price_label.place(x=10,y=50)

    name_label = Label(cart_frame, text="Customer Name:", font=('cooper black', 14), bg="#FFEBCD", fg="black")
    name_label.place(x=10,y=70)

    name_entry = Entry(cart_frame, font=('cooper black', 14))
    name_entry.place(x=180,y=70)

    cash_label = Label(cart_frame, text="Customer Cash:", font=('cooper black', 14), bg="#FFEBCD", fg="black")
    cash_label.place(x=10,y=100)

    cash_entry = Entry(cart_frame, font=('cooper black', 14))
    cash_entry.place(x=180,y=100)

    def buy_action(flavor_price_dict, chosen_flavors):
        # Retrieve customer name and customer cash from the entry
        customer_name = name_entry.get()
        customer_cash = cash_entry.get()
        user_change = float(customer_cash) - total_price

        # Check if there is sufficient stock for each item in the cart
        for flavor, price in flavor_price_dict.items():
            mycursor.execute("SELECT stocks FROM milktea2 WHERE flavor = %s", (flavor,))
            result = mycursor.fetchone()
            if result:
                stocks = result[0]
                if stocks < 1:
                    messagebox.showerror("Out of Stock", f"{flavor} is out of stock.")
                    return
                elif stocks < 2:
                    messagebox.showwarning("Low Stock", f"{flavor} has low stock.")

        # Update the stock count and store the purchase details in the database
        if total_price > 0:
            for flavor, price in flavor_price_dict.items():
                mycursor.execute("UPDATE milktea2 SET stocks = stocks - 1 WHERE flavor = %s", (flavor,))
            mydb.commit()

            sql = "INSERT INTO purchases (customer_name, total_amount, customer_cash, user_change) VALUES (%s, %s, %s, %s)"
            values = (customer_name, total_price, customer_cash, user_change)
            mycursor.execute(sql, values)
            mydb.commit()

        # Create the purchase details window
        purchase_window = Tk()
        purchase_window.title("Purchase Details")
        purchase_window.geometry("300x400")
        purchase_window.config(bg="#FFEBCD")

        # Create labels to display the customer name, customer cash, total amount, and user change
        name_label = Label(purchase_window, text="Customer Name:", font=("cooper black", 14),bg="#FFEBCD", foreground="blue")
        name_label.pack(pady=10)
        customer_label = Label(purchase_window, text=customer_name, font=("cooper black", 12),bg="#FFEBCD")
        customer_label.pack()

        cash_label = Label(purchase_window, text="Customer Cash:", font=("cooper black", 14),bg="#FFEBCD", foreground="green")
        cash_label.pack(pady=10)
        cash_value_label = Label(purchase_window, text=customer_cash, font=("cooper black", 14),bg="#FFEBCD")
        cash_value_label.pack()

        amount_label = Label(purchase_window, text="Total Amount:", font=("cooper black", 14),bg="#FFEBCD", foreground="red")
        amount_label.pack(pady=10)
        total_label = Label(purchase_window, text=str(total_price), font=("cooper black", 12),bg="#FFEBCD")
        total_label.pack()

        change_label = Label(purchase_window, text="Customer Change:", font=("cooper black", 14),bg="#FFEBCD", foreground="purple")
        change_label.pack(pady=10)
        user_change_label = Label(purchase_window, text=user_change, font=("cooper black", 12),bg="#FFEBCD")
        user_change_label.pack()

        # Create a label to display the chosen flavors or milk teas
        chosen_flavors_label = Label(purchase_window, text="Chosen Flavors:", font=("cooper black", 14),bg="#FFEBCD")
        chosen_flavors_label.pack(pady=10)

        for flavor in chosen_flavors:
            flavor_label = Label(purchase_window, text=flavor, font=("cooper black", 12),bg="#FFEBCD")
            flavor_label.pack()

        # Create a label to display the chosen flavors or milk teas


        # Add any additional widgets or functionality you want in the purchase window

        purchase_window.mainloop()

    buy_button = Button(cart_frame, text="Buy",padx=100,border=6, font=('cooper black', 14), bg="black", fg="white",
                        command=lambda: buy_action(flavor_price_dict, chosen_flavors))
    buy_button.place(x=100, y=140)



def open_admin_window():
    window.destroy()
    import admin2
    admin2.open_admin_window()


admin_button = Button(window, text="Administrator",padx=100, border=6, bg="black", fg="white", font=('cooper black', 15),command=open_admin_window)
admin_button.place(x=900, y=0)

def open_report():
    report_window = Tk()
    report_window.title("Send Report")
    report_window.geometry('450x250')

    report_window.config(bg='#FFEBCD')

    report_lbl = Label(report_window, text='Message Report', font=("cooper black", 17), bg='black', fg='white')
    report_lbl.place(x=0, y=5, width='450', height=40)

    scrollbar = Scrollbar(report_window)
    scrollbar.pack(side='right', fill='y')

    report_entry = Text(report_window, font=("cooper black", 14), width=30, height=5, wrap='word',
                        yscrollcommand=scrollbar.set)
    report_entry.place(x=50, y=60)

    scrollbar.config(command=report_entry.yview)

    def send_report():
        message = report_entry.get("1.0", "end-1c")  # Retrieve the message from the text widget

        if message:
            # Insert the report message into the database
            sql = "INSERT INTO report (messages) VALUES (%s)"
            val = (message,)
            mycursor.execute(sql, val)
            mydb.commit()

            messagebox.showinfo("Success", "Report sent successfully!")
            report_entry.delete("1.0", "end")  # Clear the report entry after sending

        else:
            messagebox.showerror("Error", "Please enter a report message.")

    send_report_btn = Button(report_window, text='Send Report', font=("cooper black", 14), bg='black', fg='white',
                             command=send_report)
    send_report_btn.place(x=150, y=170)

# Create a button to open the report window
report_button = Button(window, text="Report",padx=140, border=6, bg="black", fg="white", font=('cooper black', 15),
                       command=open_report)
report_button.place(x=900, y=50)


display_menu()
window.mainloop()