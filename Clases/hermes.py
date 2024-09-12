import os
import mysql.connector
import pandas as pd
from decouple import config, Config, RepositoryEnv

base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, '.env')

config = Config(RepositoryEnv(env_path))

class Hermes:
    def __init__(self):

        self.connection = mysql.connector.connect(host=config('HOST'), 
                               database=config('DATABASE'),
                               user=config('MYUSERNAME'),
                               password=config('PASSWORD'))
        self.cursor = self.connection.cursor()
    
    def close_connection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            
    
    def check_connection(self):
        return self.connection.is_connected()
    
    def leer_datos(self, procedure_name:str, params:list) -> pd.DataFrame:
        try:
            self.cursor.callproc(procedure_name, params)
            results = []
            columnas = []
            for result_set in self.cursor.stored_results():
                results.extend(result_set.fetchall())
                columnas = [desc[0] for desc in result_set.description]
            df = pd.DataFrame(results, columns=columnas)
            
            return df
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    
    def transformarLista(self, procedure_name:str, params:list, columna:str) -> list:
        miTabla = self.leer_datos(procedure_name, params)
        return miTabla[columna].unique().tolist()
    
    def ejecutar_procedimiento(self, procedure_name:str, params:list) -> bool:
        try:
            self.cursor.callproc(procedure_name, params)
            
            self.connection.commit()
            
            return True
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()
            return False

        
    def obtener_valor(self, procedure_name: str, params: list):
        try:
            self.cursor.callproc(procedure_name, params)
            
            result = None
            for result_set in self.cursor.stored_results():
                row = result_set.fetchone()
                if row:
                    result = row[0]  # Assuming you only need the first column's value
                
            return result
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

        
if __name__ == "__main__":
    conexionHermes = Hermes()
    r = conexionHermes.obtener_valor("validar_usuario", ['andres', 'x'])
    print(r)