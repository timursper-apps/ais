import customtkinter as ctk, config as cfg

root = ctk.CTk()
root.title("О программе")
root.geometry("810x100")

header = ctk.CTkLabel(root, text="АИС «Учёба»", font=cfg.fontHeader).grid(row=1, column=1)
alpha = ctk.CTkLabel(root, text=" (αльфа)", font=cfg.fontBasic).grid(row=1, column=2)

description = ctk.CTkLabel(root, text="АИС «Учёба» - это экосистема педагогов, учеников и школы!\nПри помощи АИС «Учёба» ученики могут оперативно просматривать оценки, учителя выставлять, а ОУ смотреть отчёты по оценкам!").place(x=0, y=30)

root.mainloop()