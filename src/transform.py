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
        
        # 1- asegurarnos de que el precio sea numérico 
        # y rellenar o limpiar posibles nulos
        df_products['price'] = pd.to_numeric(df_products['price'], errors='coerce')


        # 2. Normalización de datos anidados (Aplanar el campo 'rating')
        if 'rating' in df_products.columns:
            # Extraemos las claves del diccionario ('rate' y 'count') convirtiéndolas en un mini DataFrame
            rating_df = df_products['rating'].apply(pd.Series)
            
            # Asignamos esas métricas a nuevas columnas limpias en nuestro DataFrame principal
            df_products['rating_rate'] = rating_df['rate']
            df_products['rating_count'] = rating_df['count']
            
            # Descartamos la columna 'rating' original que tenía el diccionario completo
            df_products = df_products.drop(columns=['rating'])

        
        logging.info(f"Productos transformados correctamente. Total de filas: {len(df_products)}")
        return df_products


    def transform_carts(self):
        """
        Convierte los carritos en un DataFrame, limpia y estandariza las fechas
        (date original y loaded_at de procesamiento).
        """
        # Creamos el DataFrame a partir de la lista de carritos de la API
        df_carts = pd.DataFrame(self.raw_carts)
        
        # 1. Inyectamos la fecha/hora de procesamiento (momento en que ingresó a nuestro pipeline)
        df_carts['loaded_at'] = datetime.now()
        
        # 2. Estandarizamos la fecha original del carrito ('date') que viene de la API
        # 'errors="coerce"' convierte cualquier formato extraño o nulo en NaT (Not a Time) para evitar que rompa
        df_carts['date'] = pd.to_datetime(df_carts['date'], errors='coerce')
        
        # Opcional pero prolijo: asegurarnos también de que loaded_at sea datetime puro
        df_carts['loaded_at'] = pd.to_datetime(df_carts['loaded_at'])
        
        logging.info(f"Carritos/Órdenes transformados y fechas estandarizadas. Total de filas: {len(df_carts)}")
        return df_carts




    def transform_cart_items(self, df_carts: pd.DataFrame):
        """
        Toma el DataFrame de carritos, 'explora' la lista anidada de productos
        y genera una tabla relacional de detalle (cart_items).
        """
        items_list = []
        
        # Recorremos cada carrito para extraer sus productos individuales
        for _, row in df_carts.iterrows():
            cart_id = row['id']
            products_in_cart = row.get('products', [])
            
            for item in products_in_cart:
                items_list.append({
                    'cart_id': cart_id,
                    'product_id': item.get('productId'),
                    'quantity': item.get('quantity')
                })
        
        # Creamos el nuevo DataFrame relacional de ítems
        df_cart_items = pd.DataFrame(items_list)
        
        logging.info(f"Detalle de ítems de carritos transformado. Total de filas de detalle: {len(df_cart_items)}")
        return df_cart_items
    
    




        