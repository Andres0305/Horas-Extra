import os
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
from Clases.Horas_Extras import HorasExtra
import pandas as pd
import time

class CargaMasiva:
    def __init__(self, parent, tipo):
        
        self.carga_masiva = ctk.CTkToplevel(parent)

        self.label_conteo_registros = ctk.CTkLabel(self.carga_masiva, text=f"Conteo de registros")
        self.label_conteo_registros.grid(row=0, column=0, columnspan=2, padx=2, pady=2)

        self.progress_bar = ttk.Progressbar(self.carga_masiva, orient='horizontal', length=200, mode='determinate')
        self.progress_bar.grid(row=1, column=0, columnspan=2, padx=2, pady=2)

        self.nombre_archivo = ctk.CTkLabel(self.carga_masiva, text=f"Nombre del archivo")
        self.nombre_archivo.grid(row=2, column=0, columnspan=2, padx=2, pady=2)
        
        elejir_archivo = ctk.CTkButton(self.carga_masiva, text="Elejir Archivo", command=self.sleccionar_archivo)
        elejir_archivo.grid(row=3, column=0, padx=2, pady=2)

        if tipo == "Registro":
            cargar_archivo = ctk.CTkButton(self.carga_masiva, text="Cargar Archivo", command=self.cargar_archivo_registro)
        elif tipo == "Feriado":
            cargar_archivo = ctk.CTkButton(self.carga_masiva, text="Cargar Archivo", command=self.cargar_archivo_feriado)
        cargar_archivo.grid(row=3, column=1, padx=2, pady=2)
        self.carga_masiva.protocol("WM_DELETE_WINDOW", self.on_closing)


    def sleccionar_archivo(self):
        tipos = (('Excel', '*.xlsx'),)
        filename = fd.askopenfilename(title="Seleccionar Archivo", filetypes=tipos)
        self.nombre_archivo.configure(text=filename)

    def cargar_archivo_registro(self):
        archivo_carga = self.nombre_archivo.cget("text")
        df_carga = pd.read_excel(archivo_carga)
        df_carga['fecha'] = df_carga['fecha'].dt.strftime('%Y-%m-%d')
        df_carga['empleado'] = df_carga['empleado'].astype('str')
        df_carga['cargado'] = False
        filas = df_carga.shape[0]
        self.label_conteo_registros.configure(text=f'0 de {filas} datos cargados')
        contador = 0

        # Configure progress bar
        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = filas

        for i in df_carga.index:
            ci = df_carga['empleado'][i]
            fecha = df_carga['fecha'][i]
            horas = df_carga['horas'][i].item()
            comentario = df_carga['comentario'][i]
            if len(ci) == 9:
                ci = "0" + ci
            #try:
            mi_registro = HorasExtra(empleado=None, fecha=fecha, ci=ci)
            if mi_registro.update_registro(horas, comentario):
                contador += 1
                self.label_conteo_registros.configure(text=f'{contador} de {filas} datos cargados')
                self.progress_bar['value'] = contador
                self.carga_masiva.update()
                df_carga.loc[i, 'cargado'] = True

            time.sleep(2)
#
            #except:
            #    print("Ups, hubo un error al cargar el registro")
        if filas != contador:
            df_errores = df_carga[df_carga['cargado'] == False]
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            error_filename = os.path.join(desktop_path, "registros_con_errores.xlsx")
            df_errores.to_excel(error_filename, index=False)

            titulo = "Holy Guacamle!!"
            
            if (filas - contador) == 1:
                mensaje = f"Hay 1 registro que no se guardó. Revisa el archivo de errores en tu escritorio"
            else:
                mensaje = f"Hay {filas - contador} registros que no se guardaron. Revisa el archivo de errores en tu escritorio"
        else:
            titulo = "Cogratulations!"
            mensaje = "Todos los registros fueron guardados"

        messagebox.showinfo(titulo, mensaje)

    def cargar_archivo_feriado(self):
        archivo_carga = self.nombre_archivo.cget("text")
        df_carga = pd.read_excel(archivo_carga)
        df_carga['fecha'] = df_carga['fecha'].dt.strftime('%Y-%m-%d')
        df_carga['sucursal'] = df_carga['sucursal'].astype('str')
        df_carga['motivo'] = df_carga['motivo'].astype('str')
        df_carga['cargado'] = False
        filas = df_carga.shape[0]
        self.label_conteo_registros.configure(text=f'0 de {filas} datos cargados')
        contador = 0

        # Configure progress bar
        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = filas
        messagebox.showinfo(filas)
        for i in df_carga.index:
            fecha = df_carga['fecha'][i]
            sucursal = df_carga['sucursal'][i]
            motivo = df_carga['motivo'][i]
            print("Hey")
            #try:
            #conexionDb = DB()
            #if conexionDb.update_feriado(fecha, motivo, sucursal):
            #    contador += 1
            #    self.label_conteo_registros.configure(text=f'{contador} de {filas} datos cargados')
            #    self.progress_bar['value'] = contador
            #    self.carga_masiva.update()
            #    df_carga.loc[i, 'cargado'] = True

            time.sleep(2)

            #except:
            #    print("Ups, hubo un error al cargar el registro")
        if filas != contador:
            df_errores = df_carga[df_carga['cargado'] == False]
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            error_filename = os.path.join(desktop_path, "registros_con_errores.xlsx")
            df_errores.to_excel(error_filename, index=False)

            titulo = "Holy Guacamle!!"
            
            if (filas - contador) == 1:
                mensaje = f"Hay 1 registro que no se guardó. Revisa el archivo de errores en tu escritorio"
            else:
                mensaje = f"Hay {filas - contador} registros que no se guardaron. Revisa el archivo de errores en tu escritorio"
        else:
            titulo = "Cogratulations!"
            mensaje = "Todos los registros fueron guardados"

        messagebox.showinfo(titulo, mensaje)

    def on_closing(self):
        try:

            self.carga_masiva.destroy()
        except tk.TclError as e:

            print(f"Error during closing: {e}")
        finally:

            self.carga_masiva.quit()

    def run(self):
        self.carga_masiva.mainloop()

if __name__ == "__main__":
    carga = CargaMasiva(None, "Feriado")
    carga.run()