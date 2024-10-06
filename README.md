# Proyecto Horas Extras 

Este es un proyecto para facilitar el registro de horas extras a nivel nacional en la empresa Sucesores. La idea es centralizar en una base de datos para evitar errores de pagos.
el programa cuenta con los siguientes módulos. 

Para empezar, establezcamos algunas deficniones.
- Usuarios: Serán aquellas personas que tengan la posibilidad de cargar y leer información. Originalmente distingimos 2 tipos de usuarios, __Administrador__ y __Comun__. La diferencia
radica en lo que pueden y no hacer. Los usuarios comunes solo pueden subir información del periodo activo. Los usuarios administradores pueden añadir periodos, añadir usuarios comunes
añadir feriados y añadir empleados.
- Periodo: Hace referencia a un rango de fechas específico en los que se tomarán las horas extras para su respectiva remuneración en el rol de fin de mes. Generlamente se hace del 21 
de un mes al 20 del siguiente. Este trabajo lo debe hacer un usuario __Administrador__. Ojo, no puede haber más de un periodo activo a la vez.
- Feriados: Hace referencia a una fecha y sucursal específica en la que se celebra un feriado. Por tanto, ese día se debe pagar el doble cada hora extra. Este trabajo lo debe hacer un 
usuario __Administrador__.
- Empleados: Son todas las personas en nómina que registren horas extras. Este trabajo lo debe hacer un usuario __Administrador__.
- Plantilla: Un archivo de excel con un formato específico.
- Módulo: Es parte de la interfaz del programa y hace referencia a un grupo de vistas enfocadas en un tema particular.

## Módulo Dashboard
Es el primer módulo visible. La idea es presentar varios indicadores de forma gráfica. Claramente debe haber una distinción entre el dashboard que ve un usario comun y un administrador.

## Módulo Registro
En este módulo se registrarán todos los datos de cada sucursal y cada periodo. Constra de 3 partes. 
- __Filtros:__ En esta sección se puede seleccionar tanto la sucursal, periodo y número de semana que se va a mostrar en pantalla. Ojo, que un usuario comun está limitado a ver la sucursal
a la que pertenece y el periodo activo. Lo único que puede seleccionar es la semana que esta revisando. Finalmente, hay un boton que permite la carga masiva de informacion mediante una
plantilla.
- __Tabla:__ En esta seccion se muestra un Tree View con la infro del nombre del empleado y las horas extras de cada día. Las dos últimas columnas representan el acumulado de Horas
extras de cada tipo (50 y 100). Si se selecciona una celda, se mostraran los datos en el siguiente módulo.
- __Formulario:__ En esta seccion se mostrará el nombre de un empleado, la fecha, el número de horas y el comentario. Esta info se selecciona desde la seccion __Tabla__. Se pueden modificar
datos como el comentario o el número de horas.

## Módulo Periodo y Feriados
Este módulo sirve para crear nuevos periodos y establecer feriados. Para crear un nuevo periodo se debe seleccionar el nombre del periodo (Se establece de la forma XXXX-MM mmm), también se debe seleccionar la fecha de inicio y de fin. Se muestra así mismo, ua tabla listando los periodos e información relevante en una tabla.

Adicional, tenemos un formulario para agregar feriado, lo único que se necesita es la fecha y un comentario. Así mismo hay una tabla que muestra los periodos.
