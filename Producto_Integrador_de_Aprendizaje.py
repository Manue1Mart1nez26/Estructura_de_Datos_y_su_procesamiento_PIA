"""
PIA, Estructura de datos y su procesamiento.
"""
from typing import List
import pandas as pd
from collections import namedtuple
from datetime import datetime
import sys
import sqlite3
from sqlite3 import Error
try:
    with sqlite3.connect("EV3.db") as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS Venta (folio INTEGER NOT NULL, descripcion TEXT NOT NULL, canitdad INTEGER NOT NULL, precio INTEGER NOT NULL, total_sin_iva INTEGER NOT NULL ,total_iva INTEGER NOT NULL, fecha TEXT NOT NULL);")
            print("Tabla creada exitosamente")
except Error as e:
            print(e)
except Exception:
            print(f"Error: {sys.exc_info()[0]}")
finally:
            if conn:
                conn.close()

Ventas = namedtuple("Ventas",["Articulo","CantidadVenta","PrecioVenta","FechaVenta", "PrecioTotal"])
DiccionarioVentas = {}
DiccionarioPrecios = {"Juego de llantas 1":[400], "Juego de llantas 2":[600]}
notas_Precios = pd.DataFrame(DiccionarioPrecios)
notas_ventas = pd.DataFrame(data=DiccionarioVentas)
SEPARADOR = ("*" * 50) + "\n"
while True:
    print("\n-- Bienvenido(a) al Menú")
    print("1) Ver precios")#Lista o menu con los articulos y precios que se visualizar.
    print("2) Agregar una Venta") #Registrar una venta y dentro los articulos.
    print("3) Búsqueda específica por fecha") #Consultar una ventas por fecha| el cual imprime un reporte de venta
    print("4) Salir") #Opcion de salida del programa.

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
            try:
                with sqlite3.connect("EV3.db") as conn:
                    mi_cursor = conn.cursor()
                    for folioUnico in DiccionarioVentas:
                        cFolio = True
                        for items in DiccionarioVentas[folioUnico]:
                            if cFolio:
                                mi_cursor.execute(f"SELECT * FROM Venta WHERE EXISTS (SELECT * FROM Venta WHERE {folioUnico} = folio)")
                                registro1 = mi_cursor.fetchall()
                                if registro1:
                                    print(f"Dato con el folio: {folioUnico}, ya existe")
                                    break
                                cFolio = False
                            mi_cursor.execute(f"INSERT INTO Venta VALUES ({folioUnico},'{items.Articulo}',{items.CantidadVenta},{items.PrecioVenta},{items.PrecioVenta * items.CantidadVenta},{items.PrecioTotal},'{items.FechaVenta}');")
            except Error as e:
                print("ERROR", e)
            except Exception:
                print(f"Error: {sys.exc_info()[0]}")
            finally:
                if conn:
                    conn.close()

    elif opcionElegida == 3: #Consultar una ventas por fecha| Reporte de venta tabulado
        try:
            with sqlite3.connect("EV3.db") as conn:
                mi_cursor = conn.cursor()
                print("¿Cual es la fecha que deseas buscar?")
                Fecha = input()
                total = 0
                totalvent = 0
                print("Fecha: ", Fecha)
                mi_cursor.execute(f"SELECT * FROM Venta WHERE fecha = '{Fecha}'")
                listadoFEcha = mi_cursor.fetchall()
                print("Folio\tArticulo\tCantidad\tPrecio\ttotal_sin_iva\ttotal_iva\tfecha")
                for item in listadoFEcha:
                    print(item[0],"\t",item[1],"\t "* 2, item[2]," \t"*1, item[3],"\t"*2, item[4],"\t"*1, item[5],"\t "*1, item[6])
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

    elif opcionElegida == 4: #Salida del programa
        print("Gracias por usar el programa, buen día.")
        break

    else:
        print(SEPARADOR)
        print("Ingrese una opciónes validas indicadas en el menú")
        print(SEPARADOR)