import customtkinter as ctk
import tkinter as tk
#### VENTANAS ####
from Formularios import login
#### PANELES ####
from Formularios.Frames import sideBar, Dashboard, Registro
from Clases import usuario

# Define the Main Window class
class MainWindow(ctk.CTk):
    def __init__(self, usuario:usuario.Usuario, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario
        self.title("Panel de Administración")
        self.geometry("500x500")
        self.after(0, lambda: self.state('zoomed'))

        self.grid_rowconfigure(0, weight=1) 
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
    
        self.left_panel = sideBar.SideBar(self, show_frame_callback=self.show_frame)
        self.left_panel.grid(row=0, column=0, sticky="ns")

        self.right_panel = Dashboard.DashboardFrame(self)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)  
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_frame(self, frame_number):
        
        self.right_panel.grid_forget()

        ## Show the selected frame
        if frame_number == 1: # Dashboard
            self.right_panel = Dashboard.DashboardFrame(self)
            self.right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)  
        if frame_number == 2: #Registros
            self.right_panel = Registro.RegistroFrame(self)
            self.right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)  

    def on_closing(self):
        try:

            self.destroy()
        except tk.TclError as e:

            print(f"Error during closing: {e}")
        finally:

            self.quit()
        

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")

    login_view = login.LoginView()
    login_view.mainloop()

    if login_view.usuario is not None:
        main_window = MainWindow(login_view.usuario)
        main_window.mainloop()