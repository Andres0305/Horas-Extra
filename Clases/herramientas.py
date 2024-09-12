from datetime import datetime
from Clases.hermes import Hermes
#from hermes import Hermes

meses_minuscula = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct','nov', 'dic']
dias_esp = ['L', 'M', 'M', 'J', 'V', 'S', 'D']

def valida_usuario(nombre_usuario:str, contraseña:str) -> bool:
    conexionHemes = Hermes()
    booleano = conexionHemes.obtener_valor('validar_usuario', [nombre_usuario, contraseña])
    return booleano==1

def traduccionFechaESP_EN(fechaEsp:str, año:int) -> str:
    verdaderaFecha = fechaEsp[2:]
    dia = verdaderaFecha[:-4]
    mes = meses_minuscula.index(verdaderaFecha[-3:]) + 1
    fecha = f'{str(año)}-{mes}-{dia}'
    return fecha


if __name__ == '__main__':
    booleano = valida_usuario('andres', 'ajhsdf')
    print(booleano)
