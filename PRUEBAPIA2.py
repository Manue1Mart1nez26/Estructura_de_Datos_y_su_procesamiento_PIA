"""
Producto Integrador de Aprendizaje, Estructura de datos y su procesamiento.
"""
from typing import List
import pandas as pd
from collections import namedtuple
from datetime import date, datetime
from datetime import timedelta
import os
import sys
import sqlite3
from sqlite3 import Error

Ventas = namedtuple("Ventas",["Articulo","CantidadVenta","PrecioVenta","FechaVenta", "PrecioTotal"])
DiccionarioVentas = {}
DiccionarioPrecios = {"Juego de llantas 1":[400], "Juego de llantas 2":[600]}
notas_Precios = pd.DataFrame(DiccionarioPrecios)
notas_ventas = pd.DataFrame(data=DiccionarioVentas)
today = datetime.today()
fecha_actual = today.strftime("%d/%m/%Y")
SEPARADOR = ("*" * 50) + "\n"
while True:
    print(SEPARADOR)
    print("\n-- Bienvenido(a) al Menú")
    print("1) Ver precios")#Lista o menu con los articulos y precios que se visualizar.
    print("2) Agregar una Venta") #Registrar una venta y dentro los articulos.
    print("3) Búsqueda específica por fecha") #Consultar una ventas por fecha| el cual imprime un reporte de venta
    print("4) Crear Base de Datos en SQL") #Guarda en SQL.
    print("5) Guardar datos en SQL") #Guarda en SQL.
    print("6) Salir") #Opcion de salida del programa.
    print(SEPARADOR)
    #si se ingresa una opción de las que no esta en el menú, se le volvera a preguntar al usuario.


    opcionElegida = int(input("> "))

    if opcionElegida == 1: #Lista o menu con los articulos y precios que se visualiza
        if DiccionarioPrecios:
            print(notas_Precios)

    elif opcionElegida == 2: #Registrar una venta
        switch = True
        while switch:
            folioUnico = int(input("Porfavor ingrese el numero de venta : "))
            if folioUnico in DiccionarioVentas.keys():
                print("Ya existe en el diccionario esa folioUnico, intente nuevamente")
            else:
                Articulo = input("Porfavor ingrese su Articulo: ").capitalize()
                CantidadVenta = int(input("Porfavor ingrese la cantidad de articulos a vender: "))
                PrecioVenta = int(input("Porfavor ingrese el precio del Articulo: "))
                FechaVenta = datetime.now()
                FechaVentaFormato = FechaVenta.strftime('%d/%m/%Y')
                TuplaVenta = Ventas(Articulo,CantidadVenta,PrecioVenta,FechaVentaFormato,(PrecioVenta*CantidadVenta)*1.16)
                ListaVenta = list()
                ListaVenta.append(TuplaVenta)
                while switch:
                    PrecioPagar = (CantidadVenta * PrecioVenta)
                    PrecioPagarIVA = ((PrecioPagar * 0.16) + PrecioPagar)
                    print(f"El precio (sin IVA) a del {Articulo} es de {PrecioPagar} ")
                    print(f"El precio (con IVA) a del {Articulo} es de {PrecioPagarIVA} ")
                    print("\n-- Deseas agregar algo mas?")
                    print("1) Si")
                    print("2) No")
                    Agregarart = int(input("> "))
                    if Agregarart == 1:
                        Articulo = input("Porfavor ingrese el articulo que desea agregar: ").capitalize()
                        CantidadVenta = int(input("Porfavor ingrese la cantidad de articulos a vender: "))
                        PrecioVenta = int(input("Porfavor ingrese el precio del Articulo: "))
                        TuplaVenta = Ventas(Articulo,CantidadVenta,PrecioVenta,FechaVentaFormato,(PrecioVenta*CantidadVenta)*1.16)
                        ListaVenta.append(TuplaVenta)
                        print(f"\n-- Confirmación de datos:\nfolioUnico: {folioUnico}, Articulo: {Articulo}, Cantidad: {CantidadVenta}, Precio: {PrecioVenta}, Fecha: {FechaVentaFormato}")
                    else:
                        DiccionarioVentas[folioUnico] = ListaVenta
                        ListaTamaño = 0
                        PrecioTotal = 0
                        while ListaTamaño < len(DiccionarioVentas[folioUnico]):
                            PrecioTotal = (int(DiccionarioVentas[folioUnico][ListaTamaño].PrecioVenta)* int(DiccionarioVentas[folioUnico][ListaTamaño].CantidadVenta))+PrecioTotal
                            ListaTamaño = ListaTamaño+1
                        print(f"total de ventas: {PrecioTotal}")
                        print(f"El total con IVA aplicado es de {PrecioTotal*1.16}")
                        print ("Que le vaya bien")
                        switch = False

    elif opcionElegida == 10: #Consultar una venta
        if DiccionarioVentas:
            folioUnicoBuscado = int(input("Ingrese La venta a buscar: "))
            if folioUnicoBuscado in DiccionarioVentas:
                for Articulo in DiccionarioVentas[folioUnicoBuscado]:
                    print("\n-- Resultado de búsqueda:")
                    print(f"Articulo: {Articulo.Articulo}")
                    print(f"Cantidad: {Articulo.CantidadVenta}")
                    print(f"Precio: {Articulo.PrecioVenta}")
                    print(f"Fecha: {Articulo.FechaVenta}")
                ListaTamaño = 0
                PrecioTotal = 0
                while ListaTamaño < len(DiccionarioVentas[folioUnicoBuscado]):
                    PrecioTotal = (int(DiccionarioVentas[folioUnicoBuscado][ListaTamaño].PrecioVenta)* int(DiccionarioVentas[folioUnicoBuscado][ListaTamaño].CantidadVenta))+PrecioTotal
                    ListaTamaño = ListaTamaño+1
                print(f"Total de ventas: {PrecioTotal}")
                print(f"El total con IVA aplicado es de {PrecioTotal*1.16}")
            else:
                print("No existe La venta introducida, intente nuevamente")

    elif opcionElegida == 3: #Consultar una ventas por fecha| Reporte de venta tabulado
        total = 0
        totalvent = 0
        switch = True
        while switch: #TERMINAR ESTO NOMBRE DEL ERROR   Error: <class 'NameError'
            try:
                Fecha_buscar = input('\nIngrese la fecha que desea buscar: ')
                FechaV_conV_Buscar = datetime.strptime(Fecha_buscar, '%d/%m/%Y')
                Dia_Siguiente = datetime.today() + timedelta(days=1)
                print("0")
                if FechaV_conV_Buscar > Dia_Siguiente:
                    print(f"\nEsa fecha todavia no existe o no es valida, favor de intentarlo de nuevo")
                else:
                    break
            except Exception:
                print("\nIngresa el formato de fecha valido que es d/m/Y")
        try:
            with sqlite3.connect("EV_3.db") as conn:
                mi_cursor.execute("""SELECT FFID.folio, Venta.descripcion, Venta.canitdad, Venta.precio, Venta.total_sin_iva, Venta.total_iva, FFID.fecha \
                                    FROM FFID\
                                    INNER JOIN Venta on FFID.folio = Venta.folio\
                                    WHERE FFID.fecha = ?""",(Fecha_buscar,))
                listadoFEcha = mi_cursor.fetchall()
                if listadoFEcha:
                    print("LISTADO")
                    print(listadoFEcha)
                    print("" * 40, "PIA", "" * 40)
                    print("Articulo\tCantidad\tPrecio\ttotal_sin_iva\ttotal_iva")
                    for item in listadoFEcha:
                        print(item[1],"\t"* 2, item[2],"\t"*1, item[3],"\t"*2, item[4],"\t"*1, item[5])
                        total += item[4]
                        totalvent += item[5]
                    print(f"El total obtenido en las ventas del día es:", "$", total)
                    print(f"El total con el IVA obtenido en las ventas del día es:", "$", totalvent)
        except Error as e:
            print("ERROR", e)
        except Exception:
            print(f"Error: {sys.exc_info()[0]}")
        finally:
            if conn:
                conn.close()
                switch = False


    elif opcionElegida ==4: #Crear base de datos en SQL
        try:
            with sqlite3.connect("EV_3.db") as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("CREATE TABLE IF NOT EXISTS Folio_Fecha (folio INTEGER PRIMARY KEY, fecha TEXT NOT NULL);")
                mi_cursor.execute("CREATE TABLE IF NOT EXISTS Venta (folio INTEGER NOT NULL, descripcion TEXT NOT NULL, canitdad INTEGER NOT NULL, precio INTEGER NOT NULL, total_sin_iva INTEGER NOT NULL ,total_iva INTEGER NOT NULL, FOREIGN KEY (folio) REFERENCES Folio_Fecha(folio));")
                print("Tabla creada exitosamente")
        except Error as e:
            print(e)
        except Exception:
            print(f"Error: {sys.exc_info()[0]}")
        finally:
            if conn:
                conn.close()

    elif opcionElegida ==5: #Guardar datos en SQL
        try:
            with sqlite3.connect("EV_3.db") as conn:
                mi_cursor = conn.cursor()
                for folioUnico in DiccionarioVentas:
                    cFolio = True
                    for items in DiccionarioVentas[folioUnico]:
                        if cFolio:
                            mi_cursor.execute(f"SELECT * FROM Folio_Fecha WHERE EXISTS (SELECT * FROM Folio_Fecha WHERE {folioUnico} = folio)")
                            registro1 = mi_cursor.fetchall()
                            if registro1:
                                print(f"Dato con el folio: {folioUnico}, ya existe")
                                break
                            else:
                                mi_cursor.execute(f"INSERT INTO Folio_Fecha VALUES({folioUnico}, '{items.FechaVenta}');")
                            cFolio = False
                        mi_cursor.execute(f"INSERT INTO Venta VALUES({folioUnico},'{items.Articulo}',{items.CantidadVenta},{items.PrecioVenta},{items.PrecioVenta * items.CantidadVenta},{items.PrecioTotal});")

        except Error as e:
            print(e)
        except Exception:
            print(f"Error: {sys.exc_info()[0]}")
        finally:
            if conn:
                conn.close()

    elif opcionElegida == 6: #Salida del programa
        print("Gracias por usar el programa, buen día.")
        break

    else:
        print(SEPARADOR)
        print("Ingrese una opciónes validas indicadas en el menú")
        print(SEPARADOR)