import sqlite3
import pandas as pd
import logging
import os

class DataLoader:
    def __init__(self, db_path: str = "data/ecommerce.db"):
        """
        Constructor del cargador. Recibe la ruta donde se guardará la base de datos SQLite.
        Por defecto la guardará dentro de la carpeta 'data/'.
        """
        self.db_path = db_path
        
        # Asegurarnos de que la carpeta 'data' exista antes de conectar
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def load_data(self, df_products: pd.DataFrame, df_carts: pd.DataFrame, df_cart_items: pd.DataFrame):
        """
        Método principal que recibe los DataFrames limpios y los persiste en tablas SQLite.
        """
        try:
            logging.info(f"Iniciando proceso de carga en la base de datos: {self.db_path}")
            
            # Establecemos la conexión con SQLite
            with sqlite3.connect(self.db_path) as connection:
                
                # 1. Cargamos la tabla de productos
                # if_exists='replace' reemplaza la tabla si ya existe (ideal para pruebas repetitivas)
                # index=False evita que Pandas guarde el índice numérico (0, 1, 2...) como una columna extra
                df_products.to_sql('products', con=connection, if_exists='replace', index=False)
                logging.info(f"Tabla 'products' cargada con éxito. Filas insertadas: {len(df_products)}")
                
                # 2. Tabla de cabecera de carritos (sin la columna anidada 'products')
                # Hacemos un drop de 'products' por prolijidad para que la cabecera quede limpia
                df_carts_clean = df_carts.drop(columns=['products'], errors='ignore')
                df_carts_clean.to_sql('carts', con=connection, if_exists='replace', index=False)
                logging.info(f"Tabla 'carts' cargada con éxito. Filas: {len(df_carts_clean)}")
                
                # 3. Tabla relacional de detalle de ítems
                df_cart_items.to_sql('cart_items', con=connection, if_exists='replace', index=False)
                logging.info(f"Tabla 'cart_items' cargada con éxito. Filas: {len(df_cart_items)}")
                
                logging.info("🎉 Proceso de Carga (Load) relacional finalizado exitosamente.")
                
                logging.info("🎉 Proceso de Carga (Load) finalizado exitosamente.")
            
        except Exception as e:
            logging.error(f"❌ Error crítico al cargar los datos en la base de datos: {e}")
            raise