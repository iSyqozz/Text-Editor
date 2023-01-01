from tkinter import Canvas,FLAT,Button,INSERT,Toplevel,Checkbutton,Frame
from tkinter import VERTICAL,FALSE,LEFT,RIGHT,TRUE,BOTH,Scrollbar,Y,NW

#Custom Button Class for dynamic color change on Hover
class Custom_button(Button):
    def __init__(self,master,**kargs):
        super().__init__(master=master,**kargs,relief=FLAT)
        self.defaultbg = self['bg']
        self.defaultfg = self['fg']
        self.bind('<Enter>',self.on_enter)
        self.bind('<Leave>',self.on_leave)
    
    def on_enter(self,e):
        self['bg'] = self['activebackground']
        self['fg'] = self['activeforeground']
    
    def on_leave(self,e):
        self['bg'] = self.defaultbg
        self['fg'] = self.defaultfg

#Custom Check Button Class for dynamic color change on Hover
class Custom_Check_button(Checkbutton):
    def __init__(self,master,**kargs):
        super().__init__(master=master,**kargs,relief=FLAT)
        self.defaultbg = self['bg']
        self.defaultfg = self['fg']
        self.bind('<Enter>',self.on_enter)
        self.bind('<Leave>',self.on_leave)
    
    def on_enter(self,e):
        self['bg'] = self['activebackground']
        self['fg'] = self['activeforeground']
    
    def on_leave(self,e):
        self['bg'] = self.defaultbg
        self['fg'] = self.defaultfg
        self.select()

#vertically scrollable Frame widget
class VerticalScrolledFrame(Frame):
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        vscrollbar = Scrollbar(self, orient='vertical',bg = '#031f38',bd = 1,activebackground='#61b5ff',troughcolor='#031f38',width=10)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        def _configure_interior(event):
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

# Custom Widget for Enumerating line numbers to the left 
class TextLineNumbers(Canvas):
    def __init__(self,temp,*args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.textwidget = temp
        self.redraw()
    
    def attach(self, text_widget):
        self.textwidget = text_widget
    
    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")
        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw",font = ('Andale Mono',9),fill='#135cab',text=linenum+'>')
            i = self.textwidget.index("%s+1line" % i)
        self.after(30, self.redraw)
    
#Utility Function for getting tot_lines ,curr line and curr col 
def get_tot(editor,text_field,ln_label,curr_label):
        r,c = text_field.index(INSERT).split('.') ; c = str(int(c)+1)
        curr_label['text'] = f'ln({r}),col({c})'
        ln_label['text']='Lines: ' + (text_field.index('end-1c').split('.')[0])
        editor.after(150,lambda: get_tot(editor,text_field,ln_label,curr_label))



