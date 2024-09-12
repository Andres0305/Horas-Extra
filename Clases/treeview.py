import pandas as pd
import tkinter as tk
from tkinter import ttk

class TablaTreeView(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent)
        
        ######## ESTILO POR DEFECTO ########
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", font=("Helvetica", 10))

        # Create vertical scrollbar
        self.verscrlbar = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=self.verscrlbar.set)

        # Pack vertical scrollbar
        self.verscrlbar.pack(side="right", fill="y")

    def set_data(self, dataFrame: pd.DataFrame, agruparTotal:bool = False, filas_maximas:int = 20) -> None:
        for item in self.get_children():
            self.delete(item)

        self.configure(height=min(filas_maximas, len(dataFrame)))
        self.tag_configure("warning", background="#ed4337")  
        
        if agruparTotal:
            self["columns"] = list(dataFrame.columns)
            self.column("#0", width=10, stretch=tk.NO)  # Expand the first column to make space for the tree view
            for col in self["columns"]:
                self.heading(col, text=col)
                self.column(col, stretch=tk.NO, anchor=tk.CENTER)
            
            total_row = dataFrame[dataFrame['nombre'] == 'TOTAL'].iloc[0]
            parent_item = self.insert("", "end", values=list(total_row), tags=('total',))

            for index, row in dataFrame.iterrows():
                values = list(row) 
                if row["nombre"] == 'TOTAL':
                    pass
                elif row["totalHE50"] >= 40 or row["totalHE100"] >= 8:
                    self.insert(parent_item, "end", values=values, tags=('warning',))
                else:
                    self.insert(parent_item, "end", values=values, tags=('child',))

                # Set row colors
            self.tag_configure("total", background="#d9ead3")  
            self.tag_configure("child", background="#f9f9f9")  
        else:

            ######## COLUMNAS POR DEFECTO ########
            self.column("# 0", stretch=tk.NO, width=0)  # Remove the first column

            self["columns"] = list(dataFrame.columns)
            for columna in self["columns"]:
                self.heading(columna, text=columna)
                self.column(columna, stretch=tk.NO, anchor=tk.CENTER)
            
            for index, fila in dataFrame.iterrows():
                values = list(fila)
                if index % 2==0:
                    self.insert("", "end", values=values, tags=('filaPar',))
                else:
                    self.insert("", "end", values=values, tags=('filaImpar',))


    def clean_data(self) -> None:
        for item in self.get_children():
            self.delete(item)

    def set_estilo_verde(self):
        self.style.configure("Treeview.Heading",
                background='#4ca739',
                foreground="white",
                relief="flat")
        self.tag_configure("filaPar", background="#daf2d1")
        self.tag_configure("filaImpar", background="#b4e6a5")

    
    def set_estilo_azul(self):
        self.style.configure("Treeview.Heading",
                background='#0F9ED5',
                foreground="white",
                relief="flat")
        self.tag_configure("filaPar", background="#94DCF8")
        self.tag_configure("filaImpar", background="#CAEDFB")

    def set_ancho_columnas(self, anchos_columna: dict):
        for columna, ancho in anchos_columna.items():
            self.column(columna, width=ancho)

    def update_nombre_columna(self, renombre_columnas: dict):
        for nombre_viejo, nombre_nuevo in renombre_columnas.items():
            if nombre_viejo in self["columns"]:
                self.heading(nombre_viejo, text=nombre_nuevo)
            else:
                print(f"Column {nombre_viejo} not found in Treeview columns")


class App(tk.Tk):
    def __init__(self, dataframe: pd.DataFrame):
        super().__init__()

        self.title("Pandas DataFrame in Treeview")
        self.geometry("800x600")

        # Create a frame to hold the TreeView
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create an instance of the DataFrameTreeView
        self.tree = TablaTreeView(frame)
        self.tree.pack(side="left", fill=tk.BOTH, expand=True)

        # Set data to the TreeView
        self.tree.set_data(dataframe)

        # Example: Change the header color to blue
        self.tree.set_estilo_azul()

# Example usage:
if __name__ == "__main__":
    # Sample DataFrame
    data = {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "City": ["New York", "Los Angeles", "Chicago"]
    }
    df = pd.DataFrame(data)

    app = App(df)
    app.mainloop()
