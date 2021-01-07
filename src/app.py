import mysql.connector
import datetime
import hashlib
from tkinter import *
from tkinter import ttk
from register import *
from login import *
from tkinter import messagebox
from controlTransactions import Control
from validate_email import validate_email #pip install validate_email


class Application(object):

    def __init__(self, app):
        self.app = app
        self.app.title("Bank")

        self.app.resizable(0, 0)

        # STRINGVARS()
        self.DNI = StringVar()
        self.passwd = StringVar()
        self.IBAN_destination = StringVar()
        self.frame = LabelFrame(app)
        self.frame.grid()
        self.quanty_tranference = DoubleVar()
        self.quanty_deposit = DoubleVar()
        self.withdraw = DoubleVar()



        self.welcome = Label(self.frame, text = "LOGIN ")
        self.welcome.config(font = ("luminari", 18), fg = "light blue")
        self.welcome.grid()


        self.DNI_label = Label(self.frame, text = "DNI: ").grid()
        self.DNI_entry = Entry(self.frame, textvariable = self.DNI)
        self.DNI_entry.focus()
        self.DNI_entry.grid()

        self.passd_label = Label(self.frame, text = "Paswword: ").grid()
        self.passd_entry = Entry(self.frame, textvariable = self.passwd).grid()


        self.botton_access = Button(self.frame, text = "Access", command = self.session).grid()

        self.create_account = Button(self.frame, text="New account?", command = self.create_widget_register).grid()

    def show_balance(self):
        query = "SELECT BALANCE FROM clients WHERE DNI = %s"
        values = self.DNI.get()
        cursor.execute(query, (values, ))
        validation = cursor.fetchone()

        return validation[0]


    def session(self): # login ------------>

        try:
            hash_element = hashlib.sha256()
            hash_element.update(self.passwd.get().encode('utf-8'))

            loggin = login(self.DNI.get(), hash_element.hexdigest())

            validation_user = loggin.login_user()

            if validation_user:
                messagebox.showinfo(title="Login", message="Loggin is  successfull! ")
                self.frame.grid_remove()

                self.frame_access = LabelFrame(app)
                self.frame_access.grid(row = 0, columnspan = 2)

                self.Panel_label = Label(self.frame_access, text = "Panel Control")
                self.Panel_label.config(fg = "light blue", font = ("luminari", 18))
                self.Panel_label.grid(padx = 3, pady = 3)

                self.balance_show_label = Label(self.frame_access, text = f"Balance: {self.show_balance()} €")
                self.balance_show_label.grid()

                #OPTIONS

                self.tranference_button = Button(self.frame_access, text = "Transference", command = self.tranference).grid(padx = 5, pady = 5)
                self.deposit_button = Button(self.frame_access, text = "Deposit in my Account", command = self.deposit).grid(padx = 5, pady = 5)
                self.show_histoy_button = Button(self.frame_access, text = "View History", command = self.show_history).grid(padx = 5, pady = 5)
                self.withdraw_balance_button = Button(self.frame_access, text = "withdraw balance", command = self.withdraw_balance).grid(padx = 5, pady = 5)



            else:
                messagebox.showerror(title="Login", message="DNI OR PASSWORD INCORRECT")

        except Exception as e:
            messagebox.showerror(e)

    def query_transference(self):


        try:
            query_balance_user = "SELECT BALANCE FROM clients WHERE DNI = %s"
            values1 = self.DNI.get()
            cursor.execute(query_balance_user, (values1,))
            validation_balance = cursor.fetchall()


            if validation_balance[0][0] >= self.quanty_tranference.get() and validation_balance[0][0] >= 5: #funcion para controlar que no pueda ingresar sin saldo suficiente y que tenga minimo 5 euros apra tranferir

                query_val = "UPDATE clients SET BALANCE = BALANCE + %s WHERE IBAN = %s"
                values_val = self.quanty_tranference.get(), self.IBAN_destination.get()


                cursor.execute(query_val, (values_val) )
                validation = cursor.fetchone()


                if validation is  None:
                    db.commit()
                    messagebox.showinfo(title="Transference", message="Transference is successfull!")
                    self.refresh(self.quanty_tranference.get(), 'Transference')
                    save = Control(self.DNI.get(), "Transferencia", self.quanty_tranference.get(), self.IBAN_destination.get())
                    save.save_transactions()
                    self.top_transference.destroy()
                else:
                    messagebox.showerror(title="Error", message="Ups, an error occurred, try again later")


            else:
                messagebox.showerror(title="Error", message="not enough money")

        except Exception as e:
            messagebox.showerror(title="Error", message=e)



    def tranference(self):
        self.top_transference = Toplevel()
        self.top_transference.title = 'Tranference'

        self.IBAN_destination_label = Label(self.top_transference, text = "write the IBAN of the destination:").grid(padx = 3, pady = 3)
        self.IBAN_destination_entry = Entry(self.top_transference, textvariable = self.IBAN_destination).grid(padx = 3, pady = 3)


        self.quanty_label = Label(self.top_transference, text = "Quanty:").grid(padx = 3, pady = 3)
        self.quanty_entry = Entry(self.top_transference, textvariable = self.quanty_tranference).grid(padx = 3, pady = 3)

        self.button_save_transference = Button(self.top_transference, text = "Save", command = self.query_transference).grid(padx = 3, pady = 3)


    def deposit(self):
        self.top_deposit = Toplevel()
        self.top_deposit.title = "Deposit"

        self.quanty_deposit_label = Label(self.top_deposit, text = "Quanty: ", fg = "black").grid(padx = 3, pady = 3)
        self.quanty_deposit_entry = Entry(self.top_deposit, textvariable = self.quanty_deposit)
        self.quanty_deposit_entry.focus()
        self.quanty_deposit_entry.grid(padx = 3, pady = 3)

        self.buttom_deposit = Button(self.top_deposit, text = "Deposit", command = lambda: self.refresh(self.quanty_deposit.get(), "Deposit")).grid(padx = 3, pady = 3)

    def refresh(self, quanty,type_tr): #para actualizar el saldo (+-/type transaction) (TR, DP, WD)

        try:
            if type_tr == 'Deposit':
                sql = "UPDATE clients SET BALANCE = BALANCE + %s WHERE DNI  = %s"
                values = quanty, self.DNI.get()
                cursor.execute(sql, (values))
                db.commit()
                self.balance_show_label['text'] = f"Balance: {self.show_balance()} €"

                save = Control(self.DNI.get(), "Deposit", self.quanty_deposit.get(),"YOUR")
                save.save_transactions()
                self.top_deposit.destroy()
                return messagebox.showinfo(message="Deposit solved")

            elif type_tr == 'withdraw':
                sql = "UPDATE clients SET BALANCE = BALANCE - %s WHERE DNI  = %s"
                values = quanty, self.DNI.get()
                cursor.execute(sql, (values))
                db.commit()
                self.balance_show_label['text'] = f"Balance: {self.show_balance()} €"

                save = Control(self.DNI.get(), "withdraw balance", self.withdraw.get(), "YOUR")
                save.save_transactions()
                self.top_withdraw.destroy()
                return messagebox.showinfo(message="Withdraw balance solved")

            elif type_tr == 'Transference':
                # Refresh

                self.update_balance = "UPDATE clients SET BALANCE = BALANCE - %s WHERE DNI = %s"
                self.update_values = quanty, self.DNI.get()

                cursor.execute(self.update_balance, (self.update_values))
                db.commit()

                self.balance_show_label['text'] = f"Balance: {self.show_balance()} €"
                return messagebox.showinfo(message="Tranference Solved")

            else:
                messagebox.showerror(title="error", message="Ha ocurrido un error intentelo más tarde.")
                app.destroy()


        except Exception as e:
            return messagebox.showerror(e)



    def show_history(self):


        self.top_show = Toplevel()
        self.top_show.title = "Movements"
        self.top_show.config(bg = "light blue")

        Label(self.top_show, text = "HYSTORY",fg = "#000000", font = ("impact", 18)).grid(padx = 3, pady = 3)
        self.tree = ttk.Treeview(self.top_show, columns = ('#0', '#1', '#2'))
        self.tree.grid(padx = 10, pady = 10)
        self.tree.heading('#0', text = 'Type', anchor = CENTER)
        self.tree.heading('#1', text = 'Quanty', anchor = CENTER)
        self.tree.heading('#2', text = 'Destine', anchor = CENTER)
        self.tree.heading('#3', text = "Date", anchor = CENTER)
        self.botton_ok = Button(self.top_show, text = "OK", command = self.top_show.destroy).grid(padx = 5, pady = 5)

        try:
            query_dates = "SELECT type, quanty, destine, fecha  FROM Transact WHERE DNI_C = %s"
            cursor.execute(query_dates, (self.DNI.get(), ))
            db.commit()

            dates_transactions = cursor.fetchall()

            for dates in dates_transactions:
                self.tree.insert('', 0, text=dates[0], values=(dates[1],dates[2], dates[3]))

        except Exception as e:
            return messagebox.showerror(e)




    def withdraw_balance(self):
        self.top_withdraw = Toplevel()
        self.top_withdraw.title = "Withdraw balance"
        self.top_withdraw.config(bg = "light blue")

        Label(self.top_withdraw, text = "Quanty: ").grid(padx = 3, pady = 3)
        Entry(self.top_withdraw, textvariable = self.withdraw).grid(padx = 3, pady = 3)
        Button(self.top_withdraw, text = "Save", command = lambda: self.refresh(self.withdraw.get(), "withdraw")).grid(padx = 3, pady = 3)


        save = Control(self.DNI.get(), "withdraw_balance", self.withdraw.get(), "YOUR")
        save.save_transactions()



# REGISTER
    def create_widget_register(self):

        # VARS!!!!!!
        self.first_name_register = StringVar()
        self.last_name_register = StringVar()
        self.paswd_register = StringVar()
        self.email_register = StringVar()
        self.dni_register = StringVar()
        self.phone_register = IntVar()

        # WIDGET´´ REGISTER
        self.top_register = Toplevel()
        self.top_register.title = "Register"
        self.top_register.config(bg = "white")
        self.top_register.resizable(0,0)


        self.label_register = Label(self.top_register, text = "REGISTER ")
        self.label_register.config(font = ("luminari", 18), fg = "black")
        self.label_register.grid(padx = 3, pady = 3)

        self.label_first_username = Label(self.top_register, text = "FirstName").grid(padx = 3, pady = 3)
        self.entry_first_username = Entry(self.top_register, textvariable = self.first_name_register)
        self.entry_first_username.focus()
        self.entry_first_username.grid(padx = 3, pady = 3)

        self.label_lastname = Label(self.top_register, text = "Last Name").grid(padx = 3, pady = 3)
        self.entry_lasname = Entry(self.top_register, textvariable = self.last_name_register).grid(padx = 3, pady = 3)

        self._register_label_password = Label(self.top_register, text = "Password").grid(padx = 3, pady = 3)
        self.entry_password_register = Entry(self.top_register, textvariable = self.paswd_register).grid(padx=3, pady=3)

        self._register_label_email = Label(self.top_register, text = "Email").grid(padx = 3, pady = 3)
        self._register_email = Entry(self.top_register, textvariable = self.email_register).grid(padx = 3, pady = 3)

        self.register_dni_label = Label(self.top_register, text = "DNI").grid(padx = 3, pady = 3)
        self.register_dni_entry = Entry(self.top_register, textvariable = self.dni_register).grid(padx = 3, pady = 3)


        self.tlf_register = Label(self.top_register, text = "Number Mobile Phone").grid(padx = 3, pady = 3)
        self.tlf_register = Entry(self.top_register, textvariable = self.phone_register).grid(padx = 3, pady = 3)

        self.button_register = Button(self.top_register, text = "Save and record", command = self.save_register).grid(padx = 3, pady = 3)


    def save_register(self): #REGISTER

        first_name = self.first_name_register.get()
        last_name = self.last_name_register.get()
        password_user = self.paswd_register.get()
        email = self.email_register.get()
        dni = self.dni_register.get()
        phone = self.phone_register.get()


        if validate_email(self.email_register.get()):  #VALIDATE EMAIL (TRUE OR FALSE)
            self.register_user_ = register(first_name, last_name, password_user, email, dni, phone)
            messagebox.showinfo(message="Register is successfull!")
            self.top_register.destroy()
            return self.register_user_.new_account()

        else:
            messagebox.showerror(title="Error Email", message="Email Incorrect")



if __name__ == "__main__":
    app = Tk()
    Bank = Application(app)
    app.mainloop()

