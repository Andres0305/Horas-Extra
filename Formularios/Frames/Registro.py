from tkinter import messagebox
from Clases.Horas_Extras import HorasExtra
from Clases.treeview import TablaTreeView
import pandas as pd
import customtkinter as ctk
from Formularios.Carga_Masiva import CargaMasiva
from Clases.tabla import TablaHorasExtras
from Clases.herramientas import traduccionFechaESP_EN
class FiltrosFrame(ctk.CTkFrame):
    def __init__(self, master, revisionSucPercallback, filtroSemanacallback, *args, **kwargs):
        super().__init__(master, width=200, corner_radius=0, *args, **kwargs)
        self.master :RegistroFrame = master
        sucursales = self.master.sucursales if isinstance(self.master.sucursales, list) else [self.master.sucursales]
        periodos = self.master.periodos if isinstance(self.master.periodos, list) else [self.master.periodos]
        def carga_masiva_registro():

            carga_masiva = CargaMasiva(self,"Registro")
            carga_masiva.run()

        self.revisionSucPercallback = revisionSucPercallback
        self.filtroSemanacallback = filtroSemanacallback
        # Sucursal
        sucursalLabel = ctk.CTkLabel(self, text='Sucursal', font=("Arial", 14), anchor="w")
        self.sucursalEntry = ctk.CTkComboBox(self, values=sucursales, width=150,  command=self.revisionSucPercallback)
        self.sucursalEntry.set('')

        # Periodos
        periodoLabel = ctk.CTkLabel(self, text='Periodo', font=("Arial", 14), anchor="w")
        self.periodoEntry = ctk.CTkComboBox(self, values=periodos, width=200,  command=self.revisionSucPercallback)
        self.periodoEntry.set('')
        
        # Semanas
        semanasLabel = ctk.CTkLabel(self, text='Semana', font=("Arial", 14), anchor="w")
        self.semmanasEntry = ctk.CTkComboBox(self, values=[], width=200,  command=self.filtroSemanacallback)
        self.semmanasEntry.set('')

        # Carga Masiva
        cargaMasivaButton = ctk.CTkButton(self, text="Carga Masiva", width=60, command=carga_masiva_registro)

        sucursalLabel.grid(row=0, column=0, pady=10, padx=(20, 10), sticky="w")
        self.sucursalEntry.grid(row=0, column=1, pady=10, padx=(10, 20), sticky="w")
        periodoLabel.grid(row=0, column=2, pady=10, padx=(20, 10), sticky="w")
        self.periodoEntry.grid(row=0, column=3, pady=10, padx=(10, 20), sticky="w")
        semanasLabel.grid(row=0, column=4, pady=10, padx=(20, 10), sticky="w")
        self.semmanasEntry.grid(row=0, column=5, pady=10, padx=(10, 20), sticky="w")
        cargaMasivaButton.grid(row=0, column=6, pady=10, padx=(10,20), sticky="w")


class Tabla(ctk.CTkFrame):
    def __init__(self, master, obtenerValoresCeldacallback, *args, **kwargs):
        super().__init__(master, corner_radius=24, *args, **kwargs)
        # Initialize a Treeview or any table-like widget to hold the data
        self.treeview :TablaTreeView = TablaTreeView(self)
        self.treeview.pack(expand=True, fill="both") 
        self.treeview.set_estilo_azul()
        self.obtenerValoresCelda = obtenerValoresCeldacallback

    def set_table_data(self, data:pd.DataFrame):
        
        self.treeview.set_data(data, True, 25)
        anchos = {col: 280 if col == "nombre" else 80 for col in data.columns}
        
        self.treeview.set_ancho_columnas(anchos_columna=anchos)
        self.treeview.bind("<ButtonRelease-1>", self.obtenerValoresCelda)


class FormularioFrame(ctk.CTkFrame):
    def __init__(self, master, guardarcallback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        guardar = guardarcallback
        self.nombreCliente = ctk.CTkLabel(self, text='Nombre Empleado', font=("Arial", 14))
        self.fecha = ctk.CTkLabel(self, text='Fecha', font=("Arial", 14))
        horasLabel = ctk.CTkLabel(self, text='Horas', font=("Arial", 14))
        self.horasEntry = ctk.CTkEntry(self, width=80)
        comentarioLabel = ctk.CTkLabel(self, text='Comentario', font=("Arial", 14))
        self.comentarioEntry = ctk.CTkEntry(self, width=300)
        addButton = ctk.CTkButton(self, text="Guardar", command=guardar, width=70, height=35)

        self.nombreCliente.grid(row = 0, column=0, padx=5, pady=5, sticky="nsew")
        self.fecha.grid(row = 0, column=1, padx=5, pady=5, sticky="nsew")
        horasLabel.grid(row = 0, column=2, padx=5, pady=5, sticky="nsew")
        self.horasEntry.grid(row = 0, column=3, padx=5, pady=5, sticky="nsew")
        comentarioLabel.grid(row = 1, column=0, padx=5, pady=5, sticky="nsew")
        self.comentarioEntry.grid(row = 1, column=1, padx=5, pady=5, sticky="nsew", columnspan=2 )
        addButton.grid(row = 1, column=3, padx=5, pady=5, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)


class RegistroFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
    
        super().__init__(master, width=200, fg_color="white", corner_radius=0, *args, **kwargs)

        self.TablaGeneral:TablaHorasExtras = None
        
        def getTablaGeneral(event):
            currentSucursal = filtrosFrame.sucursalEntry.get()
            currentPeriodo = filtrosFrame.periodoEntry.get()
            tablaFrame.treeview.clean_data()
            filtrosFrame.semmanasEntry.set('')
            if currentSucursal != "" and currentPeriodo != "":
                self.TablaGeneral = TablaHorasExtras(currentSucursal,currentPeriodo)
                listaSemanas = self.TablaGeneral.getListaSemanas()
                filtrosFrame.semmanasEntry.configure(values=listaSemanas)

            else:
                print("No hay nada")

        def getTablaSemana(event):
            semana = filtrosFrame.semmanasEntry.get()
            data = self.TablaGeneral.filtrarSemana(semana)
            tablaFrame.set_table_data(data)

        def obtenerValoresCelda(event):
            try:
                item = event.widget.selection()[0]
                values = event.widget.item(item, "values") #Fila de Valores
                nombre_empleado = values[0]
                registro=None
                if nombre_empleado != "TOTAL":
                    indice_columna = event.widget.identify_column(event.x)
                    fecha_1 = event.widget.heading(indice_columna)['text']
                    ##### buscamos el año
                    periodo = filtrosFrame.periodoEntry.get()
                    año_periodo = int(periodo[:4])
                    mes_periodo = int(periodo[5:7])
                    if mes_periodo == 1 and "Dec" in fecha_1:
                        año_periodo = año_periodo - 1
                    

                    fechaReal = traduccionFechaESP_EN(fecha_1, año_periodo)
                    registro = HorasExtra(nombre_empleado, fechaReal, None)
                    #registro=None
                    
            except:
                registro = None
            finally:
                if registro is not None:
                    formularioFrame.nombreCliente.configure(text = nombre_empleado)
                    formularioFrame.fecha.configure(text = fechaReal)
                    formularioFrame.horasEntry.delete(0, ctk.END)
                    formularioFrame.horasEntry.insert(ctk.END, registro.horas)
                    formularioFrame.comentarioEntry.delete(0, ctk.END)
                    formularioFrame.comentarioEntry.insert(ctk.END, registro.comentario)
                else:
                    formularioFrame.nombreCliente.configure(text = "Nombre Empleado")
                    formularioFrame.fecha.configure(text = "Fecha")
                    formularioFrame.horasEntry.delete(0, ctk.END)
                    formularioFrame.comentarioEntry.delete(0, ctk.END)
                
        def guardar():
            nombre = formularioFrame.nombreCliente.cget("text")
            fecha = formularioFrame.fecha.cget("text")
            nueva_hora = formularioFrame.horasEntry.get()
            nuevo_comentario = formularioFrame.comentarioEntry.get()

            registro = HorasExtra(nombre, fecha, None)
            registro.update_registro(nueva_hora, nuevo_comentario)
            currentSucursal = filtrosFrame.sucursalEntry.get()
            currentPeriodo = filtrosFrame.periodoEntry.get()
            semana = filtrosFrame.semmanasEntry.get()
            self.TablaGeneral = TablaHorasExtras(currentSucursal,currentPeriodo)
            data = self.TablaGeneral.filtrarSemana(semana)
            tablaFrame.set_table_data(data)

            formularioFrame.nombreCliente.configure(text = "Nombre Empleado")
            formularioFrame.fecha.configure(text = "Fecha")
            formularioFrame.horasEntry.delete(0, ctk.END)
            formularioFrame.comentarioEntry.delete(0, ctk.END)

            messagebox.showinfo(title=None, message="Datos actualizados!!")
            
                
        self.master = master
        self.sucursales = self.master.usuario.getSucursales()
        self.periodos = self.master.usuario.getPeriodos()

        filtrosFrame = FiltrosFrame(self, getTablaGeneral, getTablaSemana)
        filtrosFrame.grid(pady=5, padx=5, row=0, column=0, sticky="nsew")

        tablaFrame = Tabla(self, obtenerValoresCelda)
        tablaFrame.grid(pady=5, padx=5, row=1, column=0, sticky="nsew")  # Place below formularioFrame

        formularioFrame = FormularioFrame(self, guardar)
        formularioFrame.grid(pady=5, padx=5, row=2, column=0, sticky="nsew")
        
        self.columnconfigure(0, weight=1)

        