from tkinter import filedialog,END
import os

def get_name(t):
    return os.path.basename(t)

def Save(Name,text_field):
    
    files = [('All Files', '*.*')]
    file = filedialog.asksaveasfile(title='Save')    
    if file:    
        Name.config(text = get_name(file.name) )
        file.write(text_field.get('0,0',END))
        file.close()

def Open(Name,text_field,END):
    
    file = filedialog.askopenfile(title = 'Open')
    if file:
        Name.config(text = get_name(file.name))
        text_field.delete('1.0',END)
        text_field.insert('1.0',file.read())
        file.close()




    