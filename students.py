import customtkinter as ctk
import sqlite3, config as cfg

conn = sqlite3.connect("marks.db")
curs = conn.cursor()

root = ctk.CTk()
root.title("Ученики")

studentName = ctk.CTkEntry(root, placeholder_text="Введите отображаемое имя ученика", width=185)
studentName.grid(row=1, column=1)

studentGrade = ctk.CTkEntry(root, placeholder_text="Введите класс ученика", width=155)
studentGrade.grid(row=1, column=2)

studentAdd = ctk.CTkButton(root, text="+", fg_color=cfg.bgLine, text_color=cfg.textLine, hover_color=cfg.hoverLine, width=25).grid(row=1, column=3)
studentRemove = ctk.CTkButton(root, text="-", fg_color=cfg.bgLine, text_color=cfg.textLine, hover_color=cfg.hoverLine, width=25).grid(row=1, column=4)

root.mainloop()