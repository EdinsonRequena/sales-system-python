from tkinter import ttk
from tkinter import *
import sqlite3

class Product:

    data_base = 'test.db'

    def __init__(self, window):
        self.window = window
        self.window.title('Sales app')

        #Frame Container
        frame = LabelFrame(self.window, text = 'Register a new product')
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

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
