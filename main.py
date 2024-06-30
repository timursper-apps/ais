import customtkinter as ctk
import os, config

root = ctk.CTk()
root.title("АИС «Учёба»")

header = ctk.CTkLabel(root, text="АИС «Учёба» - ", font=config.fontHeader).grid(row=1, column=1)
description = ctk.CTkLabel(root, text="Больше, чем журнал! αльфа", font=config.fontBasic).grid(row=1, column=2)

marksOpen = lambda : os.system("python marks.py")
studentsOpen = lambda : os.system("python students.py")
infoOpen = lambda : os.system("python information.py")

# main line
marksButton = ctk.CTkButton(root, text="Журнал", fg_color=config.bgLine, hover_color=config.hoverLine, corner_radius=config.lineRadius, command=marksOpen, text_color=config.textLine).grid(row=2, column=1, ipadx=0)
studentsButton = ctk.CTkButton(root, text="Ученики", bg_color=config.bgLine, fg_color=config.bgLine, hover_color=config.hoverLine, corner_radius=config.lineRadius, text_color=config.textLine, command=studentsOpen).grid(row=2, column=2)
infoButton = ctk.CTkButton(root, text="Информация", bg_color=config.bgLine, fg_color=config.bgLine, hover_color=config.hoverLine, corner_radius=config.lineRadius, text_color=config.textLine).grid(row=2, column=3)

root.mainloop()