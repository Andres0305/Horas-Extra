import numpy as np
import pandas as pd
from Clases.hermes import Hermes
#from hermes import Hermes
from Clases.herramientas import meses_minuscula, dias_esp
#from herramientas import meses_minuscula, dias_esp
from datetime import datetime


def formatearFecha(fecha:datetime):
    dia = fecha.day
    dia_semana = fecha.weekday()
    mes = fecha.month
    nombre_mes = meses_minuscula[mes-1]
    nombre_dia = dias_esp[dia_semana]
    return f"{nombre_dia} {dia}-{nombre_mes}"

class TablaHorasExtras:
    def __init__(self, sucursal:str, periodo:str) -> None:
        self.sucursal = sucursal
        self.periodo = periodo
        self.tabla:pd.DataFrame = pd.DataFrame()
        self.__getTabla()

    def __getTabla(self) -> None:
        conexionHermes = Hermes()
        self.tabla = conexionHermes.leer_datos('get_horas_extras', [self.periodo, self.sucursal])
        self.tabla['fecha'] = pd.to_datetime(self.tabla['fecha'], format="%Y/%m/%d")
        self.tabla['fecha2'] = self.tabla["fecha"].apply(lambda x: formatearFecha(x))
        self.tabla["semana"] = self.tabla['fecha'].dt.isocalendar().week
        self.tabla["dia_semana"] = self.tabla.apply(lambda row: 7 if str(self.sucursal) == 'SDO_SUC' and row['nombre'] != 'ALCIVAR MERA DARWIN ISMAEL' and row['fecha'].weekday() == 0 else row['fecha'].weekday(), axis=1)
        if self.sucursal != 'SDO_SUC':
            self.tabla["dia_semana"] = self.tabla['fecha'].dt.weekday + 1
        self.tabla["es_fs"] = self.tabla["dia_semana"].apply(lambda x: "HE 100" if x >= 6 else "HE 50")
        self.tabla["es_fs"] = np.where(self.tabla["es_feriado"], "HE 100", self.tabla["es_fs"])
        self.tabla["nombre_semana"] = "SEMANA " + (self.tabla["semana"] - self.tabla["semana"].min() + 1).astype(str)
        #self.tabla.to_csv("prueba.csv")
    def getListaSemanas(self) -> list:
        return self.tabla["nombre_semana"].unique().tolist()
    
    def filtrarSemana(self, semana:str) -> pd.DataFrame:
        df_filtered = self.tabla[self.tabla["nombre_semana"] == semana]
        pd_pivot = df_filtered.pivot_table(index='nombre', columns='fecha', values='horas', aggfunc='sum', fill_value=0)
        pd_pivot['totalHE50'] = df_filtered[df_filtered['es_fs'] == 'HE 50'].groupby('nombre')['horas'].sum()
        pd_pivot['totalHE100'] = df_filtered[df_filtered['es_fs'] == 'HE 100'].groupby('nombre')['horas'].sum()
        pd_pivot.reset_index(inplace=True)
        columnas = [formatearFecha(col) if type(col) != str else col for col in pd_pivot.columns]
        
        pd_pivot.columns = columnas

        fila_totales = pd_pivot.sum(numeric_only=True).to_dict()
        fila_totales['nombre'] = 'TOTAL'
        fila_totales = {'nombre': fila_totales['nombre'], **{k: fila_totales[k] for k in fila_totales if k != 'nombre'}}
        fila_totales_df = pd.DataFrame.from_dict([fila_totales])

        pd_pivot = pd.concat([pd_pivot, fila_totales_df], ignore_index=True)

        return pd_pivot
if __name__ == "__main__":
    tabla = TablaHorasExtras("CUE_SUC", "2024-02 FEB")
    pivot = tabla.filtrarSemana("SEMANA 2")
    print(pivot)

