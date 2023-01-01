from tkinter import *
from tkinter import font
from Utils import *
from FileOps import *

def run():

    #Creating editor Window and config
    editor = Tk()
    editor.title('Geno Editor')
    editor.geometry('800x900')
    editor.config(background='#031f38')
    editor.resizable(False,False)
    
    #top panel
    top_bar = Frame(master = editor, background= '#020c1a',height=80)
    top_bar.pack(fill=X)
    
    #file name on top panel
    File_name = Label(text = 'Untiteled' , master = top_bar ,bg = '#05121f', fg='white',font = ('Andale Mono',17))
    File_name.grid(column=3,row=0,padx=(140,0))

    #open Button
    open_button = Custom_button(top_bar,bg = '#05121f',cursor='plus',fg='white',text='Open',activebackground='#6ecfff',activeforeground='#05121f')
    open_button.config(height=1,width=5,justify='left',font=('Andale Mono',9))
    open_button.config(highlightcolor='#61b5ff',highlightbackground='#61b5ff',highlightthickness=1)
    
    #Save Button
    save_button = Custom_button(top_bar,bg = '#05121f',cursor='plus',fg='white',text='Save',activebackground='#6ecfff',activeforeground='#05121f')
    save_button.config(height=1,width=5,justify='left',font=('Andale Mono',9))
    save_button.config(highlightcolor='#61b5ff',highlightbackground='#61b5ff',highlightthickness=1)
    
    #saving content
    save_button.config(command = lambda : Save(File_name,text_field))
    open_button.config(command = lambda: Open(File_name,text_field,END))
    
    #display open and save buttons
    open_button.grid(row= 0, column=0,padx=(27,0),pady=(10),)
    save_button.grid(row= 0, column=1,padx=(8,0),pady=(10),)
    
    #text field and scrollbar 
    v_scroll=Scrollbar(editor, orient='vertical',bg = '#031f38',bd = 1,activebackground='#61b5ff')
    v_scroll.config(troughcolor='#031f38',width=10)
    v_scroll.pack(side=RIGHT, fill='y')

    #Text Field
    def highlight():
        text_field.tag_remove("current_line", 1.0, "end")
        text_field.tag_add("current_line", "insert linestart", "insert lineend+1c")
        editor.after(100, highlight)
    
    
    text_field = Text(master = editor,fg='white',bg='#031f38',bd = 0,highlightthickness=0,height=49)
    text_field.config(yscrollcommand=v_scroll.set,insertbackground='white',insertwidth=3,selectbackground='#61b5ff')
    text_field.pack(fill='both',padx=(25,0))
    text_field.tag_configure("current_line", background='#135cab')
    v_scroll.config(command=text_field.yview)
    highlight()
    
    #left enumeration bar
    bar = TextLineNumbers(text_field,master = editor,bg = '#05121f',)
    bar.config(bd=0,highlightthickness=0)
    bar.place(y=49,height=835,width=26)

    #bottom panel
    bar2 = Frame(master = editor, background= '#020c1a',height=17)
    bar2.pack(fill=X)
    
    #tot lines and tokens indicator
    tot = Label(master = bar2,text = 'Lines: 1',fg = 'white',bg = '#020c1a',font=('Andale Mono',9))
    tot.place(x = 715)

    #curr line and curr col
    curr = Label(master = bar2,text = 'ln(1),col(1)',fg = 'white',bg = '#020c1a',font=('Andale Mono',9))
    curr.place(x = 615)
    
    # dynamic indication lines and cols
    get_tot(editor, text_field, tot,curr)


    #toggle evaluation for checks
    def eval_check(box,root):
        def Toggle(b):
            if b['text'][0] != '⬤':
                b['text'] = '⬤ ' + b['text']
            else:
                b['text'] = b['text'][2:]
        
        if box['text'] != 'Change Font':
            Toggle(box) 

        if 'display line count' in box['text'] :
            if box['text'][0] != '⬤': 
                tot.place_forget()
            else:
                tot.place(x=715) 
        elif 'display curr position' in box['text']:
            if box['text'][0] != '⬤': 
                curr.place_forget()
            else: 
                curr.place(x=615)
        elif 'display Bottom Pannel' in box['text']:
            if box['text'][0] != '⬤': 
                bar2.pack_forget()
                bar.place(y=49,height=850,width=26)
            else: 
                bar2.pack(fill=X)
                bar.place(y=49,height=835,width=26)

    #opening preferences menu
    def pref_window(t):

        def on_closing():
            t['state'] = NORMAL ; root.destroy()

        t['state'] = DISABLED
        root = Toplevel()
        root.geometry('200x95')
        root.resizable(False,False)
        root.config(background='#031f38')
        root.title('Preferences')

        root.protocol('WM_DELETE_WINDOW',on_closing)
        check1 = IntVar() ; check2 = IntVar()
        btn2 = Custom_button(root,bg = '#05121f',cursor='arrow',fg='white',text='⬤ display line count',activebackground='#6ecfff',activeforeground='#05121f')
        btn3 = Custom_button(root,bg = '#05121f',cursor='arrow',fg='white',text='⬤ display curr position',activebackground='#6ecfff',activeforeground='#05121f')        
        btn4 = Custom_button(root,bg = '#05121f',cursor='arrow',fg='white',text='⬤ display Bottom Pannel',activebackground='#6ecfff',activeforeground='#05121f')                
        btn2.pack(fill=X) ;btn3.pack(fill=X) ; btn4.pack(fill=X)
        btn2.config(command=lambda:eval_check(btn2,root))
        btn3.config(command=lambda:eval_check(btn3,root))
        btn4.config(command=lambda:eval_check(btn4,root))
    
    
    # Find and Replace Functionality
    def find_and_replace_text(text_field,b):

        def find_matches(pattern,repl):

            text_field.tag_remove('found','1.0',END)
            if not pattern or not repl: return

            idx = '1.0'
            while True:
                # searches for desired string from index 1
                idx = text_field.search(pattern, idx, nocase = 1,
                stopindex = END)

                if not idx: break

                # last index sum of current index and
                # length of text
                lastidx = '% s+% dc' % (idx, len(pattern))

                text_field.delete(idx, lastidx)
                text_field.insert(idx, repl)

                lastidx = '% s+% dc' % (idx, len(repl))

            # overwrite 'Found' at idx
                text_field.tag_add('found', idx, lastidx)
                idx = lastidx

            # mark located string as red

            text_field.tag_config('found', foreground ='#42f5a7')

           
        def on_close():
            b['state'] = NORMAL
            text_field.tag_remove('found','1.0',END)
            root.destroy()

        b['state'] = DISABLED
        root = Toplevel()
        root.geometry('200x100')
        root.resizable(False,False)
        root.config(background='#020c1a')
        root.title('Find')
        root.protocol('WM_DELETE_WINDOW',on_close)

        placeholder1 = Entry(master = root,insertbackground='white',font=('Andale Mono',7) ,width=14,bg = '#020c1a',fg = 'white',highlightcolor='#61b5ff',highlightbackground='#61b5ff',highlightthickness=1)
        placeholder1.grid(row=0 , column=1 , padx=(0,80),pady=(8,0))
        placeholder2 = Entry(master = root,insertbackground='white',font=('Andale Mono',7) ,width=14,bg = '#020c1a',fg = 'white',highlightcolor='#61b5ff',highlightbackground='#61b5ff',highlightthickness=1)
        placeholder2.grid(row=1 , column=1 , padx=(0,80),pady=(8,0))
        
        label1 = Label(font=('Andale Mono',7),master = root,fg = 'white', text = 'Find :' ,bg ='#020c1a' )
        label2 = Label(font=('Andale Mono',7),master = root,fg = 'white', text = 'Replace with :' ,bg ='#020c1a' )
        label1.grid(row=0,column=0, padx=(0,20),pady=(8,0))
        label2.grid(row=1,column=0, padx=(0,20),pady=(8,0))
        
        search_button = Custom_button(root,font=('Andale Mono',12),bg = '#05121f',cursor='arrow',fg='white',text='Confirm',activebackground='#6ecfff',activeforeground='#05121f')
        search_button.config(highlightcolor='#61b5ff',highlightthickness=1,highlightbackground='#61b5ff')
        search_button.place(x = 52, y=60)
        search_button.config(command = lambda: find_matches(placeholder1.get(),placeholder2.get()))
    
    # Find Functionality
    def find_text(text_field,b):

        def find_matches(pattern):

            text_field.tag_remove('found','1.0',END)
            if not pattern: return
            idx = '1.0'
            while True:
                # searches for desired string from index 1
                idx = text_field.search(pattern, idx, nocase = 1,
                stopindex = END)

                if not idx: break

                # last index sum of current index and
                # length of text
                lastidx = '% s+% dc' % (idx, len(pattern))

            # overwrite 'Found' at idx
                text_field.tag_add('found', idx, lastidx)
                idx = lastidx

            # mark located string as red

            text_field.tag_config('found', foreground ='yellow')

           
        def on_close():
            b['state'] = NORMAL
            text_field.tag_remove('found','1.0',END)
            root.destroy()

        b['state'] = DISABLED
        root = Toplevel()
        root.geometry('200x30')
        root.resizable(False,False)
        root.config(background='#020c1a')
        root.title('Find')
        root.protocol('WM_DELETE_WINDOW',on_close)

        placeholder = Entry(master = root ,width=19,bg = '#020c1a',fg = 'white',highlightcolor='#61b5ff',highlightbackground='#61b5ff',highlightthickness=1)
        placeholder.pack(side = LEFT,padx=(8,0))

        search_button = Custom_button(master=root, text = '⚲',bd = 0 ,bg ='#020c1a' ,fg = '#61b5ff',highlightthickness=0,activebackground='#020c1a',activeforeground = 'white')
        search_button.pack(side = LEFT,padx=(8,0))
        search_button.config(command = lambda: find_matches(placeholder.get()))



    
    #dropdown menu
    drop_frame = Frame(master = editor,height = 150,width=100,bg ='#05121f')
    choices = ['Save As','Find','Find & Replace','Preferences']
    
    count = 0
    buttons = []
    for choice in choices:
        buttons.append(Custom_button(drop_frame,bg = '#05121f',cursor='arrow',fg='white',text=choice,anchor='w',activebackground='#6ecfff',activeforeground='#05121f'))
        buttons[-1].config(highlightcolor='#61b5ff',highlightbackground='#61b5ff',highlightthickness=1)
        buttons[-1].config(height=1,width=10,font=('Andale Mono',7))
        buttons[-1].grid(column=0,row=count,ipadx=9) ; count+=1
    
    buttons[0].config(command=lambda : Save(File_name,text_field))
    buttons[3].config(command=lambda : pref_window(buttons[3]))
    buttons[1].config(command = lambda: find_text(text_field,buttons[1]))
    buttons[2].config(command = lambda: find_and_replace_text(text_field,buttons[2]))
    
    #dropdown button
    def show_widget():
        drop_frame.place(x=160,y=39)
        drop_button.config(command=hide_widget)
    def hide_widget():
        drop_frame.place_forget()
        drop_button.config(command=show_widget)

    drop_button=Custom_button(top_bar,bg = '#05121f',cursor='plus',fg='white',text='▼',activebackground='#6ecfff',activeforeground='#05121f')
    drop_button.config(height=1,width=1,justify='left',font=('Andale Mono',9))
    drop_button.config(highlightcolor='#61b5ff',highlightbackground='#61b5ff',highlightthickness=1)
    drop_button.config(command=show_widget)
    
    drop_button.grid(row= 0, column=2,padx=(0,0),pady=(10),)
    
    #mainloop
    editor.mainloop()


#for debugging
def test():
    pass

#start of aplication
if __name__ == '__main__':
    run()
    #test()