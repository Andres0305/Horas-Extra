from . import hermes

class Usuario:
    def __init__(self, nombre_usuario:str) -> None:
        self.__id_usuario = None
        self.nombre_usuario = nombre_usuario
        self.__sucursal = None
        self.__conexion_hermes = hermes.Hermes()
        self.__is_admin = None
        self.__periodo = None
        self.llenar_datos()
    
    def llenar_datos(self) -> None:
        datos_usuario = self.__conexion_hermes.leer_datos('get_usuario_by_username', [self.nombre_usuario])
        self.__id_usuario = datos_usuario.loc[0, 'id']
        self.__sucursal = datos_usuario.loc[0, 'sucursal']
        self.__is_admin = datos_usuario.loc[0, 'admin']
        self.__periodo = datos_usuario.loc[0, 'periodo']

        if self.__is_admin == 1:
            self.__sucursal = self.__conexion_hermes.transformarLista(procedure_name='get_sucursales', params=[], columna="sucursal")
            self.__periodo = self.__conexion_hermes.transformarLista(procedure_name='get_periodos', params=[], columna="nombre")

    def es_Admin(self) -> bool:
        return self.__is_admin == 1
    
    def getSucursales(self) -> list:
        return self.__sucursal
    
    def getPeriodos(self) -> list:
        return self.__periodo
    
    

if __name__ == '__main__':
    nuevoUsuario = Usuario('Karen')
    print(nuevoUsuario.es_Admin())