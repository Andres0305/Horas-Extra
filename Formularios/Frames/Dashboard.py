import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from PIL import Image
from Clases import Dashboard
from Clases.hermes import base_dir

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, width=200, fg_color="white", corner_radius=0, *args, **kwargs)
        
        self.master = master

        image_path_empleado = os.path.join(base_dir, '..', 'assets', 'empleados.png')
        image_path_reloj = os.path.join(base_dir, '..', 'assets', 'clock.png')


        dashboard = Dashboard.Dashboard()
        welcome_label = ctk.CTkLabel(self, text="Bienvenido al Dashboard", font=("Arial", 24))
        welcome_label.pack(pady=20)

        ################# FRAME 1 (CARTAS) #################
        frame_1_cartas = ctk.CTkFrame(self, width=self.winfo_width(), height=100, fg_color="white", corner_radius=0)
        frame_1_cartas.pack(pady=10, padx=10)

        ######### CARTA EMPLEADO #########
        empleados_label_card = ctk.CTkLabel(frame_1_cartas, text="", width=200, height=100, fg_color="orange", corner_radius=30)
        empleados_label_card.grid(row=0, column=0, padx=20)
        
        valor = dashboard.get_empleados_activos()
        #### VALOR ####
        empleados_valor = ctk.CTkLabel(empleados_label_card, text=valor, font=("Arial", 30), text_color="white", corner_radius=100)
        empleados_valor.place(x=100, y=45)

        #### TITULO ####
        empleados_text = ctk.CTkLabel(empleados_label_card, text="Empleados Activos", font=("Arial", 14), text_color="white", corner_radius=100)
        empleados_text.place(x=10, y=5)

        #### ICONO ####
        empleados_icon = ctk.CTkImage(light_image=Image.open(image_path_empleado), dark_image=Image.open(image_path_empleado), size=(50, 50))
        empleados_icono = ctk.CTkLabel(empleados_label_card, 
                                       image=empleados_icon, 
                                       text="")
        empleados_icono.place(x=50,y=40)

        ######### CARTA HE 50 #########
        he50_label_card = ctk.CTkLabel(frame_1_cartas, text="", width=200, height=100, fg_color="blue", corner_radius=30)
        he50_label_card.grid(row=0, column=1, padx=20)

        he100, he50 = dashboard.get_total_horas()

        #### VALOR ####
        he50_valor = ctk.CTkLabel(he50_label_card, text=he50, font=("Arial", 30), text_color="white", corner_radius=100)
        he50_valor.place(x=90, y=45)

        #### TITULO ####
        he50_text = ctk.CTkLabel(he50_label_card, text="Horas Extras 50", font=("Arial", 14), text_color="white", corner_radius=100)
        he50_text.place(x=10, y=5)

        #### ICONO ####
        he50_icon = ctk.CTkImage(light_image=Image.open(image_path_reloj), dark_image=Image.open(image_path_reloj), size=(50, 50))
        he50_icono = ctk.CTkLabel(he50_label_card, 
                                  image=he50_icon, 
                                  text="")
        he50_icono.place(x=40,y=40)

        ######### CARTA HE 100 #########
        he100_label_card = ctk.CTkLabel(frame_1_cartas, text="", width=200, height=100, fg_color="chartreuse2", corner_radius=30)
        he100_label_card.grid(row=0, column=2, padx=20)
        #### VALOR ####
        he100_valor = ctk.CTkLabel(he100_label_card, text=he100, font=("Arial", 30), text_color="white", corner_radius=100)
        he100_valor.place(x=90, y=45)

        #### TITULO ####
        he100_text = ctk.CTkLabel(he100_label_card, text="Horas Extras 100", font=("Arial", 14), text_color="white", corner_radius=100)
        he100_text.place(x=10, y=5)

        #### ICONO ####
        he100_icon = ctk.CTkImage(light_image=Image.open(image_path_reloj), dark_image=Image.open(image_path_reloj), size=(50, 50))
        he100_icono = ctk.CTkLabel(he100_label_card, 
                                   image=he100_icon, 
                                   text="")
        he100_icono.place(x=40,y=40)

        # Create a frame to contain both the bar chart and the pie chart
        chart_frame = ctk.CTkFrame(self, fg_color="white")
        chart_frame.pack(pady=10)

        # Bar chart
        fig_bar, _ = dashboard.barra_semanas_horas()
        canvas_bar = FigureCanvasTkAgg(fig_bar, master=chart_frame)
        canvas_bar.draw()
        canvas_bar.get_tk_widget().pack(side="left", padx=20, pady=20)  # Pack canvas to the left with padding

        # Pie chart
        fig_pie = dashboard.pastel_departamento_horas()
        canvas_pie = FigureCanvasTkAgg(fig_pie, master=chart_frame)
        canvas_pie.draw()
        canvas_pie.get_tk_widget().pack(side="left", padx=5, pady=20)  # Pack canvas to the left with padding