import socket
import time
import threading
import customtkinter as CTk
from tkinter import messagebox


class ClientApp(CTk.CTk):

    def __init__(self):
        super().__init__()
        self.app = CTk.CTk()
        self.geometry = self.app.geometry("1400x750")
        self.resizible = self.app.resizable(False, False)
        self.title = self.app.title("crap")
        

    def start_app(self):
        username = messagebox.askquestion(title="Username", message="FFF")

        self.app.mainloop()




if __name__ == "__main__":
    ClientApp().start_app()
    ClientApp().start_process()