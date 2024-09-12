import numpy as np
import matplotlib.pyplot as plt
from . import hermes
import pandas as pd

class Dashboard:
    def __init__(self):
        db = hermes.Hermes()
        self.__df = db.leer_datos("get_info_by_user",["AMB_SUC"])
        #####
        self.__df['fecha'] = pd.to_datetime(self.__df['fecha'], format="%Y/%m/%d")

        self.__df["dia_semana"] = self.__df['fecha'].dt.weekday + 1

        self.__df["es_fs"] = self.__df["dia_semana"].apply(lambda x: "HE 100" if x >= 6 else "HE 50")

        self.__df["semana"] = self.__df['fecha'].dt.isocalendar().week

        min_semana = self.__df.semana.min()

        self.__df["nombre_semana"] = "Semana " + (self.__df["semana"]- min_semana).astype(str)

    def get_empleados_activos(self):
        
        return len(self.__df["nombre"].unique())
    
    def get_total_horas(self):
        pivot_df = self.__df.groupby(by="es_fs").horas.agg('sum')
        pivot_df = pivot_df.sort_index()
        return pivot_df.values
    
    def barra_semanas_horas(self):
        pivot_df = self.__df.pivot_table(columns="nombre_semana", index="es_fs", values="horas", aggfunc="sum")
    
        pivot_df = pivot_df.reindex(columns=["Semana 1", "Semana 2", "Semana 3", "Semana 4", "Semana 5"])

        es_fs = pivot_df.index
        semanas = pivot_df.columns
        data = pivot_df.values

        fig, ax = plt.subplots(figsize=(6, 7))

        colors = {'HE 100': 'red', 'HE 50': 'green'}  

        width = 0.35  
        x = np.arange(len(semanas)) 

        for i, es_fs_value in enumerate(es_fs):
            rects = ax.bar(x + i * width, data[i], width, label=es_fs_value, color=colors[es_fs_value])
            ax.bar_label(rects, padding=3, label_type='center', color='white')

        ax.set_xlabel('Semana')
        ax.set_ylabel('Horas')
        ax.set_title('Horas Extra por Semana y Tipo (HE 50 vs HE 100)')
        ax.set_xticks(x + width * (len(es_fs) - 1) / 2)  
        ax.set_xticklabels(semanas)
        ax.legend()
        #plt.show()
        return fig, ax

    def pastel_departamento_horas(self):
        pivot_df = self.__df.groupby(by="departamento").horas.sum()
        pivot_df = pivot_df[pivot_df != 0.0]

        # Data
        labels = pivot_df.index.tolist()
        data = pivot_df.values

        # Create a donut chart
        fig, ax = plt.subplots(figsize=(7, 5))
        wedges, texts, autotexts = ax.pie(data, 
                                          labels=labels, 
                                          autopct='%1.1f%%', 
                                          pctdistance=0.84,
                                          startangle=90, 
                                          wedgeprops=dict(width=0.3), 
                                          textprops=dict(color="black"))

        # Annotation properties
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                bbox=bbox_props, zorder=0, va="center")

        # Set title
        ax.set_title('Horas por Departamento')

        return fig

    def ranking_horas_50(self):
        df_ranked = self.__df[self.__df["es_fs"]=="HE 50"].groupby(by=["nombre", "departamento"]).horas.sum()
        df_ranked = df_ranked.sort_values(ascending=False).reset_index()
        df_ranked = df_ranked.head(5)
        print(df_ranked)
        return df_ranked
    
    def ranking_horas_100(self):
        df_ranked = self.__df[self.__df["es_fs"]=="HE 100"].groupby(by=["nombre", "departamento"]).horas.sum()
        df_ranked = df_ranked.sort_values(ascending=False).reset_index()
        df_ranked = df_ranked.head(5)
        print(df_ranked)
        return df_ranked
        