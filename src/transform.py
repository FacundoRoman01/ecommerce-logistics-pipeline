import pandas as pd
import logging
from datetime import datetime

class DataTransformer:

    #constructor
    def __init__(self, raw_data: dict):
        """
        Recibe el diccionario con los datos crudos (products y carts) 
        extraídos por el módulo anterior.
        """
        self.raw_products = raw_data.get("products", [])
        self.raw_carts = raw_data.get("carts", [])

    def transform_products(self):
        """
        Convierte los productos en un DataFrame y realiza una limpieza básica.
        """
        
        
        # Creamos el DataFrame a partir de la lista de productos
        df_products = pd.DataFrame(self.raw_products)
        
        # asegurarnos de que el precio sea numérico 
        # y rellenar o limpiar posibles nulos
        df_products['price'] = pd.to_numeric(df_products['price'], errors='coerce')
        
        logging.info(f"Productos transformados correctamente. Total de filas: {len(df_products)}")
        return df_products


    def transform_carts(self):
        """
        Convierte los carritos en un DataFrame y agrega una marca de tiempo 
        ya que la API no provee el campo de fecha original.
        """
        
        # Creamos el DataFrame a partir de la lista de carritos de la API
        df_carts = pd.DataFrame(self.raw_carts)
        
        # Inyectamos una fecha/hora de procesamiento (simulando el momento en que ingresó la orden)
        df_carts['loaded_at'] = datetime.now()
        
        logging.info(f"Carritos/Órdenes transformados correctamente. Total de filas: {len(df_carts)}")
        return df_carts
    
    




        