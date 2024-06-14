import psycopg2
from tkinter import *
from tkinter import messagebox, simpledialog


class BankSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Bank Management System")
        self.master.geometry("400x300")

        # Database connection
        self.conn = psycopg2.connect(
            dbname="bank_system",
            user="postgres",
            password="root",
            host="localhost"
        )
        self.cursor = self.conn.cursor()

        # Create Account Frame
        self.create_account_frame = Frame(self.master, bg='#F0F0F0')
        self.create_account_frame.pack(pady=20)

        # Labels
        self.name_label = Label(self.create_account_frame, text="Name:", font=('Arial', 12), bg='#F0F0F0')
        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.age_label = Label(self.create_account_frame, text="Age:", font=('Arial', 12), bg='#F0F0F0')
        self.age_label.grid(row=1, column=0, padx=10, pady=10)
        self.salary_label = Label(self.create_account_frame, text="Salary:", font=('Arial', 12), bg='#F0F0F0')
        self.salary_label.grid(row=2, column=0, padx=10, pady=10)
        self.pin_label = Label(self.create_account_frame, text="PIN:", font=('Arial', 12), bg='#F0F0F0')
        self.pin_label.grid(row=3, column=0, padx=10, pady=10)

        # Entries
        self.name_entry = Entry(self.create_account_frame, font=('Arial', 12), bg='#FFFFFF', relief='solid',
                                borderwidth=1)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.age_entry = Entry(self.create_account_frame, font=('Arial', 12), bg='#FFFFFF', relief='solid',
                               borderwidth=1)
        self.age_entry.grid(row=1, column=1, padx=10, pady=10)
        self.salary_entry = Entry(self.create_account_frame, font=('Arial', 12), bg='#FFFFFF', relief='solid',
                                  borderwidth=1)
        self.salary_entry.grid(row=2, column=1, padx=10, pady=10)
        self.pin_entry = Entry(self.create_account_frame, show="*", font=('Arial', 12), bg='#FFFFFF', relief='solid',
                               borderwidth=1)
        self.pin_entry.grid(row=3, column=1, padx=10, pady=10)

        # Create account button
        self.create_account_button = Button(self.create_account_frame, text="Create Account", font=('Arial', 12),
                                            bg='#4CAF50', fg='#FFFFFF', activebackground='#2E8B57',
                                            activeforeground='#FFFFFF', relief='raised', borderwidth=0,
                                            command=self.create_account)
        self.create_account_button.grid(row=4, column=1, pady=20)

        # Login Frame
        self.login_frame = Frame(self.master, bg="#FFFFFF")
        self.login_frame.pack(pady=20)
        self.login_name_label = Label(self.login_frame, text="Name:", font=("Arial", 14), bg="#FFFFFF")
        self.login_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.login_name_entry = Entry(self.login_frame, width=30, font=("Arial", 14))
        self.login_name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.login_pin_label = Label(self.login_frame, text="PIN:", font=("Arial", 14), bg="#FFFFFF")
        self.login_pin_label.grid(row=1, column=0, padx=10, pady=10)
        self.login_pin_entry = Entry(self.login_frame, show="*", width=30, font=("Arial", 14))
        self.login_pin_entry.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = Button(self.login_frame, text="Login", command=self.login, font=('Arial', 12), bg='#4CAF50',
                                   fg='#FFFFFF', activebackground='#2E8B57', activeforeground='#FFFFFF',
                                   relief='raised', borderwidth=0)
        self.login_button.grid(row=2, column=1, padx=10, pady=10)
        self.master.bind('<Return>', self.login)  # Allow login with "Enter" key

        # User Details Frame
        self.user_details_frame = Frame(self.master)

        # Labels
        label_style = {"fg": "green", "font": ("Calibri", 14)}

        self.name_label2 = Label(self.user_details_frame, text="Name:", **label_style)
        self.name_label2.grid(row=0, column=1, padx=10, pady=10)

        self.age_label2 = Label(self.user_details_frame, text="Age:", **label_style)
        self.age_label2.grid(row=1, column=1, padx=10, pady=10)

        self.salary_label2 = Label(self.user_details_frame, text="Salary:", **label_style)
        self.salary_label2.grid(row=2, column=1, padx=10, pady=10)

        self.current_balance_label = Label(self.user_details_frame, text="Current Balance:", **label_style)
        self.current_balance_label.grid(row=3, column=1, padx=10, pady=10)

        # Buttons
        self.view_transaction_button = Button(self.user_details_frame, text="View Transaction Log",
                                              command=self.view_transaction_log, bg="green", fg="white")
        self.view_transaction_button.grid(row=4, column=0, padx=10, pady=10)
        self.deposit_button = Button(self.user_details_frame, text="Deposit", command=self.deposit, bg="yellow",
                                     fg="black")
        self.deposit_button.grid(row=4, column=1, padx=10, pady=10)
        self.withdraw_button = Button(self.user_details_frame, text="Withdraw", command=self.withdraw, bg="orange",
                                      fg="white")
        self.withdraw_button.grid(row=4, column=2, padx=10, pady=10)
        self.logout_button = Button(self.user_details_frame, text="Logout", command=self.logout, bg="red", fg="white")
        self.logout_button.grid(row=4, column=3, padx=10, pady=10)

        # Initialize user data
        self.current_user_data = {}

    def create_account(self):
        # Get user input
        name = self.name_entry.get()
        age = self.age_entry.get()
        salary = self.salary_entry.get()
        pin = self.pin_entry.get()

        # Validate input
        if not name or not age or not salary or not pin:
            messagebox.showerror("Error", "All fields are required!")
            return
        if not age.isdigit():
            messagebox.showerror("Error", "Age must be a number!")
            return
        if not salary.isdigit():
            messagebox.showerror("Error", "Salary must be a number!")
            return
        if not pin.isdigit() or len(pin) != 4:
            messagebox.showerror("Error", "PIN must be a 4-digit number!")
            return

        # Insert user data into database
        try:
            self.cursor.execute(
                "INSERT INTO users (name, age, salary, pin, balance, transaction_log) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, age, salary, pin, 0, [])
            )
            self.conn.commit()
        except psycopg2.IntegrityError:
            self.conn.rollback()
            messagebox.showerror("Error", "PIN already exists!")
            return

        # Clear input fields
        self.name_entry.delete(0, END)
        self.age_entry.delete(0, END)
        self.salary_entry.delete(0, END)
        self.pin_entry.delete(0, END)

        messagebox.showinfo("Success", "Account created successfully!")

    def login(self, event=None):
        # Get user input
        name = self.login_name_entry.get()
        pin = self.login_pin_entry.get()

        # Fetch user data from database
        self.cursor.execute("SELECT * FROM users WHERE pin=%s AND name=%s", (pin, name))
        user_data = self.cursor.fetchone()

        if user_data:
            # Set current user data
            self.current_user_data = {
                'id': user_data[0],
                'name': user_data[1],
                'age': user_data[2],
                'salary': user_data[3],
                'pin': user_data[4],
                'balance': user_data[5],
                'transaction_log': user_data[6] or []
            }

            # Show the user details frame and update the labels
            self.user_details_frame.pack(pady=20)

            self.name_label2['text'] = f"Name: {self.current_user_data['name']}"
            self.age_label2['text'] = f"Age: {self.current_user_data['age']}"
            self.salary_label2['text'] = f"Salary: {self.current_user_data['salary']}"
            self.current_balance_label['text'] = f"Current Balance: {self.current_user_data['balance']}"

            # Hide login and create account frames
            self.login_frame.pack_forget()
            self.create_account_frame.pack_forget()
        else:
            # Show an error message box if the user does not exist
            messagebox.showerror("Error", "Invalid PIN or UserName")

    def deposit(self):
        # Get user input
        amount = simpledialog.askstring("Deposit", "Enter amount:")

        # Validate input
        if not amount or not amount.isdigit() or int(amount) <= 0:
            messagebox.showerror("Error", "Invalid input!")
            return

        amount = int(amount)
        current_balance = self.current_user_data['balance'] + amount

        # Update database
        self.cursor.execute("UPDATE users SET balance=%s WHERE id=%s", (current_balance, self.current_user_data['id']))
        self.conn.commit()

        # Update current user data and balance label
        self.current_user_data['balance'] = current_balance
        self.current_balance_label.config(text="Current Balance: " + str(current_balance))

        # Add transaction to transaction log
        transaction = f"Deposit: +{amount}, New Balance: {current_balance}"
        self.current_user_data['transaction_log'].append(transaction)
        self.cursor.execute("UPDATE users SET transaction_log=%s WHERE id=%s",
                            (self.current_user_data['transaction_log'], self.current_user_data['id']))
        self.conn.commit()

    def withdraw(self):
        # Get user input
        amount = simpledialog.askstring("Withdraw", "Enter amount:")

        # Validate input
        if not amount or not amount.isdigit() or int(amount) <= 0:
            messagebox.showerror("Error", "Invalid amount!")
            return

        amount = int(amount)
        current_balance = self.current_user_data['balance']

        # Check if there is enough balance
        if amount > current_balance:
            messagebox.showerror("Error", "Insufficient balance!")
            return

        # Subtract amount from current balance
        current_balance -= amount

        # Update database
        self.cursor.execute("UPDATE users SET balance=%s WHERE id=%s", (current_balance, self.current_user_data['id']))
        self.conn.commit()

        # Update current user data and balance label
        self.current_user_data['balance'] = current_balance
        self.current_balance_label.config(text="Current Balance: " + str(current_balance))

        # Add transaction to transaction log
        transaction = f"Withdraw: -{amount}, New Balance: {current_balance}"
        self.current_user_data['transaction_log'].append(transaction)
        self.cursor.execute("UPDATE users SET transaction_log=%s WHERE id=%s",
                            (self.current_user_data['transaction_log'], self.current_user_data['id']))
        self.conn.commit()

    def view_transaction_log(self):
        # Create transaction log window
        transaction_log_window = Toplevel(self.master)
        transaction_log_window.title("Transaction Log")

        # Create transaction log frame
        transaction_log_frame = Frame(transaction_log_window)
        transaction_log_frame.pack(padx=10, pady=10)

        # Create transaction log label
        transaction_log_label = Label(transaction_log_frame, text="Transaction Log:")
        transaction_log_label.grid(row=0, column=0, padx=10, pady=10)

        # Create transaction log listbox
        transaction_log_listbox = Listbox(transaction_log_frame, width=50)
        transaction_log_listbox.grid(row=1, column=0, padx=10, pady=10)

        # Insert all transactions into listbox
        for transaction in self.current_user_data['transaction_log']:
            transaction_log_listbox.insert(END, transaction)

    def logout(self):
        # Clear user data
        self.current_user_data = {}

        # Clear input fields
        self.login_name_entry.delete(0, END)
        self.login_pin_entry.delete(0, END)

        # Show login and create account frames
        self.user_details_frame.pack_forget()
        self.create_account_frame.pack(pady=20)
        self.login_frame.pack()

    def _del_(self):
        # Check if self.conn and self.cursor exist before attempting to close them
        if hasattr(self, 'conn') and hasattr(self, 'cursor'):
            self.cursor.close()
            self.conn.close()


def main():
    # Create a Tk object
    root = Tk()

    # Create an instance of the BankSystem class
    bank_system = BankSystem(root)

    # Start the mainloop
    root.mainloop()


if __name__ == '__main__':
    main()