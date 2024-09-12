import os
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from Clases import hermes, usuario

def valida_usuario(nombre_usuario:str, contraseña:str) -> bool:
    conexionHemes = hermes.Hermes()
    booleano = conexionHemes.obtener_valor('validar_usuario', [nombre_usuario, contraseña])
    return booleano==1 
# Define the Login class as a top-level window
class LoginView(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario :usuario.Usuario = None


        self.title("Login")
        self.geometry("380x270")

        self.grab_set() 
        self.update_idletasks()
        image_path_login = os.path.join(hermes.base_dir, '..', 'assets', 'login image.png')
        ############# IMAGEN #############
        my_image = ctk.CTkImage(light_image=Image.open(image_path_login),
                                dark_image=Image.open(image_path_login),
                                size=(200, 200))

        welcome_label = ctk.CTkLabel(self, text="Bienvenido")
        welcome_label.grid(row=0, column=0, padx=10, pady=10, columnspan = 2)

        image_label = ctk.CTkLabel(self, text="", image=my_image)
        image_label.grid(row=1, column=0, rowspan=5, padx=10, pady=10)

        # Create and place widgets
        self.username_label = ctk.CTkLabel(self, text="Username:")
        self.username_label.grid(row=1, column=1, padx=10, pady=1)
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.grid(row=2, column=1, padx=10, pady=1)

        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.grid(row=3, column=1, padx=10, pady=1)
        self.password_entry = ctk.CTkEntry(self, show="*")  # Show '*' for password input
        self.password_entry.grid(row=4, column=1, padx=10, pady=0.5)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.grid(row=5, column=1, padx=10, pady=10)  

    def login(self):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        if valida_usuario(entered_username, entered_password):
            self.usuario = usuario.Usuario(entered_username)
            self.destroy()
        else:
            print("No Validado")

if __name__ == '__main__':
    app = LoginView()
    app.mainloop()
        
