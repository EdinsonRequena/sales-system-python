from tkinter import ttk
from tkinter import *
import sqlite3

class Product:

    data_base = 'test.db'

    def __init__(self, window):
        self.window = window
        self.window.title('Sales app')

        #Frame Container
        frame = LabelFrame(self.window, text = 'Welcome to the sales system')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        #Name Input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        #Price Input
        Label(frame, text ='Price: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        #Button for save product
        ttk.Button(frame, text = 'Save Product', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)
        ttk.Button(frame, text = 'Delete Product', command = self.delete_product).grid(row = 4, columnspan = 2, sticky = W + E)
        ttk.Button(frame, text = 'Edit Product', command = self.update_product).grid(row = 5, columnspan = 2, sticky = W + E)

        #Messages
        self.message = Label(text = '', fg = 'blue')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        #Table
        self.table = ttk.Treeview(height = 10, columns = 2)
        self.table.grid(row = 4, column = 0, columnspan = 2)
        self.table.heading('#0', text = 'Name', anchor = CENTER)
        self.table.heading('#1', text = 'Price', anchor = CENTER)

        self.obtain_product()


    def execute_query(self, query, data = ()):
        with sqlite3.connect(self.data_base) as act:
            cursor = act.cursor()
            result = cursor.execute(query, data)
            act.commit()
        return result


    def obtain_product(self):
        # cleared the table
        elements = self.table.get_children()
        for element in elements:
            print(elements)
            self.table.delete(element)

        # consulting data
        query =  'SELECT * FROM products ORDER BY name DESC'
        database_rows = self.execute_query(query)

        for rows in database_rows:
            self.table.insert('', 0, text = rows[1], values = rows[2])


    def validate(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0
    

    def add_product(self):
        if self.validate():
            query = 'INSERT INTO products VALUES (NULL, ?, ?)'
            data = (self.name.get(), self.price.get())
            self.execute_query(query, data)
            self.message['text'] = f'the {self.name.get()} has been successfully added at a price of $ {self.price.get()}'
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message['text'] = 'enter the required data'
        self.obtain_product()


    def select_product(self):
        self.message['text'] = ''
        try:
            self.table.item(self.table.selection())['text'][0]
        except IndexError as error:
            self.message['text'] = 'Please select a product'
            return
        self.message['text'] = ''


    def delete_product(self):
        self.select_product()

        self.name = self.table.item(self.table.selection())['text']
        query = 'DELETE FROM products WHERE name = ?'
        self.execute_query(query, (self.name, ))
        self.message['text'] = f'Product {self.name} has been deleted successfuly'

        self.obtain_product()


    def update_product(self):
        self.select_product()

        self.edit_name = self.table.item(self.table.selection())['text']
        self.edit_price = self.table.item(self.table.selection())['values'][0]

        self.update_interface()

    
    def update_interface(self):
        self.edit_window = Toplevel()
        self.edit_window.title = 'Edit The Product'
        
        # Current name
        Label(self.edit_window, text = 'Current Name: ').grid(row = 0, column = 1)
        Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = self.edit_name), state = 'readonly').grid(row = 0, column = 2)
        
        # New name label
        Label(self.edit_window, text = 'Enter the New Name: ').grid(row = 1, column = 1)

        # New name entry
        new_name = Entry(self.edit_window)
        new_name.grid(row = 1, column = 2)

        # Current price
        Label(self.edit_window, text = 'Current Price: ').grid(row = 2, column = 1)
        Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = self.edit_price), state = 'readonly').grid(row = 2, column = 2)

        # New Price label
        Label(self.edit_window, text = 'Enter the New Price').grid(row = 3, column = 1)

        # New price entry
        new_price = Entry(self.edit_window)
        new_price.grid(row = 3, column = 2)

        # Button to save changes
        Button(self.edit_window, text = 'Save Changes', command = lambda: self.save_changes)


    def save_changes(self, current_name, new_name, current_price, new_price):
        query = 'UPDATE products SET name = ?, price = ? WHERE name = ? AND price = ?'
        data = (current_name, new_name, current_price, new_price)
        self.execute_query(query, data)
        self.edit_window.destroy()
        self.mesage['text'] = f'Product {self.name} has been update succesfuly'
        self.obtain_product()

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
