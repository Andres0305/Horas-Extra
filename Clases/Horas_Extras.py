import datetime
from Clases.hermes import Hermes
#from hermes import Hermes

conexionHermes = Hermes()

class HorasExtra:
    def __init__(self, empleado=None, fecha=None, ci=None) -> None:
        if empleado==None:
            tabla  = conexionHermes.leer_datos('get_registro_by_ci_fecha', [ci, fecha])
            new_empleado, horas, comentario, es_feriado, sucursal = tabla.loc[0, ['nombre', 'horas', 'comentario', 'es_feriado', 'sucursal']].tolist()
            self.empleado = new_empleado
            self.ci = ci

        else:
            tabla  = conexionHermes.leer_datos('get_registro_by_emp_fecha', [empleado, fecha])

            new_ci, horas, comentario, es_feriado, sucursal = tabla.loc[0, ['id_empleado', 'horas', 'comentario', 'es_feriado', 'sucursal']].tolist()
            self.empleado = empleado
            self.ci = new_ci

        
        self.fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d')
        self.horas = horas
        self.comentario = comentario
        self.es_feriado = es_feriado
        self.sucursal = sucursal
    
    def update_registro(self, hora, comentario):
        try:
            conexionHermes.ejecutar_procedimiento('update_registro_by_emp_fecha', [self.ci, self.fecha, hora, comentario])
            return True
        except:
            print("ups, hubo un error actualizando los datos")
            return False
        
    def es_H100(self):
        if self.sucursal != "SDO_SUC" or self.empleado == 'ALCIVAR MERA DARWIN ISMAEL':
            return self.fecha.weekday() >= 5 or self.es_feriado
        else:
            return self.fecha.weekday() == 0 or self.fecha.weekday() == 6 or self.es_feriado



if __name__ == "__main__":
    registro = HorasExtra("MENDOZA MOLINA ARTURO RAFAEL", '2024-01-24', None)
    print("empleado", registro.empleado)
    print("ci", registro.ci)
    print("fecha", registro.fecha)
    print("horas", registro.horas)
    print("comentario", registro.comentario)
    registro2 = HorasExtra(None, '2024-01-22', '1203429483')
    print("empleado", registro2.empleado)
    print("fecha", registro2.ci)
    print("fecha", registro2.fecha)
    print("horas", registro2.horas)
    print("comentario", registro2.comentario)
    print("ci", registro.ci)