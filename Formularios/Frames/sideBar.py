import os
import customtkinter as ctk
from Clases.hermes import base_dir
from PIL import Image

class SideBar(ctk.CTkFrame):
    def __init__(self, master, show_frame_callback, *args, **kwargs):
        super().__init__(master, width=200, fg_color="black", corner_radius=0, *args, **kwargs)
        self.show_frame_callback = show_frame_callback
        self.master = master

        image_path_user = os.path.join(base_dir, '..', 'assets', 'user image.jpg')
        image_path_dashboard = os.path.join(base_dir, '..', 'assets', 'dashboard icon.png')
        image_path_tabla = os.path.join(base_dir, '..', 'assets', 'data table icon.png')
        image_path_periodo = os.path.join(base_dir, '..', 'assets', 'periodo icon.png')
        image_path_feriado = os.path.join(base_dir, '..', 'assets', 'feriado icon.png')
        image_path_empleado = os.path.join(base_dir, '..', 'assets', 'empleado icon.png')

        ######################### IMAGEN USUARIO ##########################
        user_image = ctk.CTkImage(light_image=Image.open(image_path_user),
                                   dark_image=Image.open(image_path_user),
                                   size=(100, 100))
        image_label = ctk.CTkLabel(self, 
                                    image=user_image, 
                                    text="", 
                                    corner_radius=50, 
                                    width=4)
        image_label.pack(pady=30, padx=90)

        ######################### NOMBRE USUARIO ##########################
        nombre_usuario_label = ctk.CTkLabel(self, 
                                            text=self.master.usuario.nombre_usuario,
                                            font=("Arial", 40),
                                            text_color="white", 
                                            anchor="w")
        nombre_usuario_label.pack(pady=30, padx=90, fill="x")

        ########################## SIDEBAR OPTIONS ##########################
        # Option 1: Dashboard
        dashboard_frame = ctk.CTkFrame(self, width=220, height=60, fg_color="transparent")
        dashboard_frame.pack(pady=(30, 10), padx=30, fill="x")

        dashboard_icon = ctk.CTkImage(light_image=Image.open(image_path_dashboard),
                                       dark_image=Image.open(image_path_dashboard),
                                       size=(40, 40))
        dashboard_button = ctk.CTkButton(dashboard_frame, 
                                          image=dashboard_icon, 
                                          text="     Dashboard", 
                                          font=("Arial", 25),
                                          text_color="white", 
                                          anchor="w", 
                                          compound="left",
                                          fg_color="transparent",
                                          bg_color="transparent",
                                          command=lambda: self.show_frame_callback(1))
        dashboard_button.pack(side="left", padx=10, fill="x", expand=True)

        # Option 2: Registros
        registro_frame = ctk.CTkFrame(self, width=220, height=60, fg_color="transparent")
        registro_frame.pack(pady=(10, 30), padx=30, fill="x")

        registro_icon = ctk.CTkImage(light_image=Image.open(image_path_tabla),
                                      dark_image=Image.open(image_path_tabla),
                                      size=(40, 40))
        registro_button = ctk.CTkButton(registro_frame, 
                                         image=registro_icon, 
                                         text="     Registros", 
                                         font=("Arial", 25),
                                         text_color="white", 
                                         anchor="w", 
                                         compound="left",
                                         fg_color="transparent",
                                         bg_color="transparent",
                                         command=lambda: self.show_frame_callback(2))
        registro_button.pack(side="left", padx=10, fill="x", expand=True)
        ############## OPCIONES DE ADMIN ##############
        if self.master.usuario.es_Admin:
            # Option 3: Periodos 
            periodo_frame = ctk.CTkFrame(self, width=220, height=60, fg_color="transparent")
            periodo_frame.pack(pady=(10, 30), padx=30, fill="x")

            periodo_icon = ctk.CTkImage(light_image=Image.open(image_path_periodo),
                                        dark_image=Image.open(image_path_periodo),
                                        size=(40, 40))
            periodo_button = ctk.CTkButton(periodo_frame, 
                                            image=periodo_icon, 
                                            text="     Periodos", 
                                            font=("Arial", 25),
                                            text_color="white", 
                                            anchor="w", 
                                            compound="left",
                                            fg_color="transparent",
                                            bg_color="transparent",)
            periodo_button.pack(side="left", padx=10, fill="x", expand=True)
            # Option 4: Feriados 
            feriado_frame = ctk.CTkFrame(self, width=220, height=60, fg_color="transparent")
            feriado_frame.pack(pady=(10, 30), padx=30, fill="x")

            feriado_icon = ctk.CTkImage(light_image=Image.open(image_path_feriado),
                                        dark_image=Image.open(image_path_feriado),
                                        size=(40, 40))
            feriado_button = ctk.CTkButton(feriado_frame, 
                                            image=feriado_icon, 
                                            text="     Feriados", 
                                            font=("Arial", 25),
                                            text_color="white", 
                                            anchor="w", 
                                            compound="left",
                                            fg_color="transparent",
                                            bg_color="transparent",)
            feriado_button.pack(side="left", padx=10, fill="x", expand=True)
            # Option 4: Empleados 
            empleado_frame = ctk.CTkFrame(self, width=220, height=60, fg_color="transparent")
            empleado_frame.pack(pady=(10, 30), padx=30, fill="x")

            empleado_icon = ctk.CTkImage(light_image=Image.open(image_path_empleado),
                                        dark_image=Image.open(image_path_empleado),
                                        size=(40, 40))
            empleado_button = ctk.CTkButton(empleado_frame, 
                                            image=empleado_icon, 
                                            text="     Empleados", 
                                            font=("Arial", 25),
                                            text_color="white", 
                                            anchor="w", 
                                            compound="left",
                                            fg_color="transparent",
                                            bg_color="transparent",)
            empleado_button.pack(side="left", padx=10, fill="x", expand=True)