import socket
import time
import threading
import customtkinter as CTk


class App(CTk.CTk):

    def __init__(self):
        super().__init__()
        self.root = CTk.CTk()
        self.rootwidth = self.root.winfo_screenwidth()
        self.rootheight = self.root.winfo_screenheight()
        self.root.geometry(str(self.rootwidth) + "x" + str(self.rootheight))
        self.root.title("crap")
        self.root.resizable(True, True)

        self.tabview = CTk.CTkTabview(self.root,
                                      width=self.rootwidth - 10,
                                      height=self.rootheight - 10)
        self.tabview.add("Chat")
        self.tabview.add("Settings")
        self.tabview.set("Settings")
        self.tabview.pack()

        #Chat frame:
        self.ChatFrame = CTk.CTkFrame(self.tabview.tab("Chat"),
                                      width=self.rootwidth - 20,
                                      height=self.rootheight - 60)
        self.ChatFrameTextbox = CTk.CTkTextbox(self.ChatFrame,
                                               width=150,
                                               height=600,
                                               font=("Arial", 20))
        self.ChatFrameTextbox.pack(fill="both", expand=True)
        self.ChatFrame.pack(fill="both", expand=True)

        self.ChatFrameInput = CTk.CTkEntry(self.ChatFrame, font=("Arial", 24))
        self.ChatFrameInput.pack(fill="both", expand=True, side="bottom")
        self.ChatFrameInput.bind("<Return>", self.getmessage)

        #Settings frame
        self.SettingsFrame = CTk.CTkFrame(self.tabview.tab("Settings"))

        self.HostLabel = CTk.CTkLabel(self.SettingsFrame,
                                      text="Host:",
                                      font=("Arial", 30, "bold"))
        self.HostLabel.pack(pady=(self.rootheight / 4, 0))

        self.HostEntry = CTk.CTkEntry(self.SettingsFrame,
                                      justify="center",
                                      width=30,
                                      font=("Times", 30))
        self.HostEntry.pack(expand=True, fill="both", padx=600, pady=10)

        self.Portlabel = CTk.CTkLabel(self.SettingsFrame,
                                      text="Port:",
                                      font=("Arial", 30, "bold"))
        self.Portlabel.pack(padx=(10, 0))
        
        self.PortEntry = CTk.CTkEntry(self.SettingsFrame,
                                      justify="center",
                                      width=10,
                                      font=("Arial", 30))
        self.PortEntry.pack(expand=True, fill="both", padx=600, pady=10)

        self.Userlabel = CTk.CTkLabel(self.SettingsFrame,
                                      text="User:",
                                      font=("Arial", 30, "bold"))
        self.Userlabel.pack(padx=(10, 0))

        self.UserEntry = CTk.CTkEntry(self.SettingsFrame,
                                      justify="center",
                                      width=10,
                                      font=("Arial", 30))
        self.UserEntry.pack(expand=True, fill="both", padx=600, pady=10)

        self.ConnectButton = CTk.CTkButton(self.SettingsFrame,
                                           text="Connect",
                                           font=("Arial", 50),
                                           command=self.connect_to_chat)
        self.ConnectButton.pack(pady=20)

        self.SettingsFrame.pack(fill="both", expand=False)


        self.shutdown = False
        self.join = False 
        

        self.clientHost = socket.gethostbyname(socket.gethostname())
        self.clientPort = 0

        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind((self.clientHost, self.clientPort))
        self.client.setblocking(0)

        self.message = ""

    


    def getmessage(self, event):
        if self.ChatFrameInput.get() != "":
            self.message = self.ChatFrameInput.get()
            self.ChatFrameInput.delete(0, CTk.END)

    def receiving(self, name, sock):
        while self.shutdown == False:
            try:
                while True:
                    data, addr = self.sock.recvfrom(1024)
                    self.ChatFrameTextbox.insert(CTk.END, data.decode("utf-8"))

                    time.sleep(0.2)

            except:
                pass

    def connect_to_chat(self):

        if self.HostEntry.get() != "" and self.PortEntry.get(
        ) != "" and self.UserEntry.get() != "":
            self.Host = self.HostEntry.get()
            self.Port = int(self.PortEntry.get())
            self.Username = self.UserEntry.get()

            self.server = (self.Host, self.Port)
            self.tabview.set("Chat")

            self.shutdown = False
            self.join = False 
            
            
            
            self.RcVng = threading.Thread(target=self.receiving,
                                      args=("RecvThread", self.client), daemon=True)

            self.RcVng.start()

            while self.shutdown == False:

                if self.join == False:
                    
                    self.client.sendto(("[" + self.Username +
                                            "] => join chat ").encode("utf-8"),
                                           self.server)
                    self.join = True

                else:
                    try:
                        
                            if self.message != "":
                                self.client.sendto(("[" + self.Username + "] :: " +
                                                self.message).encode("utf-8"),
                                               self.server)

                                time.sleep(0.2)
                            pass

                    except:
                        self.client.sendto("[" + self.Username +
                                       "] => leave.".encode("utf-8"), self.server)
                        self.shutdown == True

            self.RcVng.join()
            self.client.close()

    def run(self):
        self.root.mainloop()
        


#192.168.1.8
#7000

App().run()
