import customtkinter
from CTkTable import *
import sqlite3
from tkinter import Canvas
#import pandas as pd
import pandas as pd

class CTkXYFrame(customtkinter.CTkFrame):
    def __init__(self,
                 master: any,
                 width: int = 100,
                 height: int = 100,
                 scrollbar_width: int = 16,
                 scrollbar_fg_color = None,
                 scrollbar_button_color = None,
                 scrollbar_button_hover_color = None,
                 **kwargs):

        self.parent_frame = customtkinter.CTkFrame(master=master, **kwargs)
        self.bg_color = self.parent_frame.cget("fg_color")
        self.xy_canvas = Canvas(self.parent_frame, width=width, height=height,
                                bg=self.parent_frame._apply_appearance_mode(self.bg_color),
                                borderwidth=0, highlightthickness=0)
        self.parent_frame.rowconfigure(0,weight=1)
        self.parent_frame.columnconfigure(0,weight=1)
        
        customtkinter.CTkFrame.__init__(self, master=self.xy_canvas, fg_color=self.parent_frame.cget("fg_color"),
                                        bg_color=self.parent_frame.cget("fg_color"))
        self.window_id = self.xy_canvas.create_window((0,0), window=self, anchor="nw")
        
        self.vsb = customtkinter.CTkScrollbar(self.parent_frame, orientation="vertical", command=self.xy_canvas.yview,
                                              fg_color=scrollbar_fg_color, button_color=scrollbar_button_color,
                                              button_hover_color=scrollbar_button_hover_color, width=scrollbar_width)
        self.hsb = customtkinter.CTkScrollbar(self.parent_frame, orientation="horizontal", command=self.xy_canvas.xview,
                                              fg_color=scrollbar_fg_color, button_color=scrollbar_button_color,
                                              button_hover_color=scrollbar_button_hover_color, height=scrollbar_width)
        
        self.xy_canvas.configure(yscrollcommand=lambda x,y: self.dynamic_scrollbar_vsb(x,y),
                                 xscrollcommand=lambda x,y: self.dynamic_scrollbar_hsb(x,y))
        self.xy_canvas.grid(row=0, column=0, sticky="nsew", padx=(7,0), pady=(7,0))
        
        self.bind("<Configure>", lambda event, canvas=self.xy_canvas: self.onFrameConfigure(canvas))
        self.xy_canvas.bind_all("<MouseWheel>", lambda e: self._on_mousewheel(e.delta, e.widget), add="+")
        self.xy_canvas.bind_all("<Shift-MouseWheel>", lambda e: self._on_mousewheel_shift(e.delta, e.widget), add="+")
        self.xy_canvas.bind_all("<Button-4>", lambda e: self._on_mousewheel(120, e.widget), add="+")
        self.xy_canvas.bind_all("<Button-5>", lambda e: self._on_mousewheel(-120, e.widget), add="+")
        self.xy_canvas.bind_all("<Shift-Button-4>", lambda e: self._on_mousewheel_shift(120, e.widget), add="+")
        self.xy_canvas.bind_all("<Shift-Button-5>", lambda e: self._on_mousewheel_shift(-120, e.widget), add="+")

        if type(master) is customtkinter.CTkScrollableFrame:
            master.check_if_master_is_canvas = self.disable_contentscroll
            
    def destroy(self):
        customtkinter.CTkFrame.destroy(self)
        self.parent_frame.destroy()

    def _set_appearance_mode(self, mode_string):
        super()._set_appearance_mode(mode_string)
        self.xy_canvas.config(bg=self.parent_frame._apply_appearance_mode(self.bg_color))

    def check_if_master_is_canvas(self, widget):
        if widget == self.xy_canvas:
            return True
        elif widget.master is not None:
            return self.check_if_master_is_canvas(widget.master)
        else:
            return False
        
    def disable_contentscroll(self, widget):
        if widget == self.xy_canvas:
            return True
        else:
            return False
        
    def dynamic_scrollbar_vsb(self, x, y):
        if float(x)==0.0 and float(y)==1.0:
            self.vsb.grid_forget()
        else:
            self.vsb.grid(row=0, column=1, rowspan=2, sticky="nse", pady=5)
        self.vsb.set(x,y)
        
    def dynamic_scrollbar_hsb(self, x, y):
        if float(x)==0.0 and float(y)==1.0:
            self.hsb.grid_forget()
        else:
            self.hsb.grid(row=1, column=0, sticky="nwe", padx=(5,0))
        self.hsb.set(x,y)
        
    def onFrameConfigure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    def _on_mousewheel(self, event, widget):
        if self.check_if_master_is_canvas(widget):
            self.xy_canvas.yview_scroll(int(-1*(event/120)), "units")
        
    def _on_mousewheel_shift(self, event, widget):
        if self.check_if_master_is_canvas(widget):
            self.xy_canvas.xview_scroll(int(-1*(event/120)), "units")
        
    def pack(self, **kwargs):
        self.parent_frame.pack(**kwargs)

    def place(self, **kwargs):
        self.parent_frame.place(**kwargs)

    def grid(self, **kwargs):
        self.parent_frame.grid(**kwargs)

    def pack_forget(self):
        self.parent_frame.pack_forget()

    def place_forget(self, **kwargs):
        self.parent_frame.place_forget()

    def grid_forget(self, **kwargs):
        self.parent_frame.grid_forget()

    def grid_remove(self, **kwargs):
        self.parent_frame.grid_remove()

    def grid_propagate(self, **kwargs):
        self.parent_frame.grid_propagate()

    def grid_info(self, **kwargs):
        return self.parent_frame.grid_info()

    def lift(self, aboveThis=None):
        self.parent_frame.lift(aboveThis)

    def lower(self, belowThis=None):
        self.parent_frame.lower(belowThis)
        
    def configure(self, **kwargs):
        if "fg_color" in kwargs:
            self.bg_color = kwargs["fg_color"]
            self.xy_canvas.config(bg=self.bg_color)
            self.configure(fg_color=self.bg_color)
        if "width" in kwargs:
            self.xy_canvas.config(width=kwargs["width"])
        if "height" in kwargs:
            self.xy_canvas.config(height=kwargs["height"])
        self.parent_frame.configure(**kwargs)

conn = sqlite3.connect("marks.db")
curs = conn.cursor()
grade = "4А"
schoolname = "test"
tableNameVar = ""

root = customtkinter.CTk()
root.title("Редактирование оценок")
root.state("zoomed")
columnNumber = 0

studentsTableList = [["Число"],
                    ["Тип работы"]]

marksTableList = [[""],
                  [""]]

curs.execute("SELECT name FROM students WHERE grade == ?", (grade,))
students1 = curs.fetchall()
students2 = []
#print(students1)

for student in students1:
    students2.append(student)
for student in students2:
    studentsTableList.append([student])
    marksTableList.append([""])

frame = CTkXYFrame(root, width=1000, height=450)
frame.grid(row=1)

tableName = customtkinter.CTkEntry(root, placeholder_text="Введите название журнала", width=250)
tableName.grid(row=1, column=3, sticky="n")

#vertScroll = ctk.CTkScrollbar(root, orientation="vertical").grid(row=1, column=2)

studentTable = ""
marksTable = ""

def loadTable(x=1):
    global tableNameVar, studentsTable, marksTable, columnNumber
    tableNameVar = tableName.get().lower()

    try:
        curs.execute(f"""
        CREATE TABLE {tableNameVar}_{grade}_{schoolname}(
            data{columnNumber} TEXT
        )
""")
        conn.commit()
        columnNumber += 1
    except:
        curs.execute(f"SELECT * FROM {tableNameVar}_{grade}_{schoolname}")
        print(curs.fetchall())

        studentsTable = CTkTable(frame, values=studentsTableList, height=5)
        studentsTable.grid(row=1, column=1)

        marksTable = CTkTable(frame, values=marksTableList, write=1, height=5)
        marksTable.grid(row = 1, column=2)

def addColumn():
    global columnNumber
    curs.execute(f"ALTER TABLE {tableNameVar}_{grade}_{schoolname} ADD COLUMN data{columnNumber}")
    conn.commit()

    columnNumber += 1

def saveChanges(x = 1):
    try:
        curs.execute(f"DROP TABLE {tableNameVar}_{grade}_{schoolname}")
    except:
        pass

    global studentsTableList, marksTableList, students2

    students = []
    for student in students2:
        students.append(student[0][0])
    print(students)

    marksTableList = marksTable.get()

    table = studentsTableList
    
    df = pd.DataFrame(data=table)
    df[1] = marksTableList
    print(df)
    df.to_excel(f"{tableNameVar}_{grade}_{schoolname}.xlsx", index=False)

#tableLoad = customtkinter.CTkButton(root, text="Загрузить журнал", command=loadTable).place(y=1500)
#tableSave = customtkinter.CTkButton(root, text="Сохранить журнал", command=saveTable).place(x=1200, y=0)

root.bind("<KeyPress-Insert>", loadTable)
root.bind("<ButtonPress-2>", lambda _ : marksTable.add_column(""))
root.bind("<ButtonPress-3>", saveChanges)

root.mainloop()