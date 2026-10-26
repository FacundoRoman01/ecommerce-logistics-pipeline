import logging
from src.extract import DataExtractor
from src.transform import DataTransformer
from src.load import DataLoader

# Configuración de los logs principales del orquestador
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    """
    Función principal que coordina el flujo completo del pipeline de datos:
    Extracción -> Transformación -> (Carga)
    """
    logging.info("=== INICIANDO PIPELINE DE DATOS ===")
    
    try:
        # PASO 1: EXTRACCIÓN
        logging.info("Paso 1: Iniciando fase de Extracción...")
        extractor = DataExtractor()
        raw_data = extractor.extract_ecommerce_data()
        
        # PASO 2: TRANSFORMACIÓN
        logging.info("Paso 2: Iniciando fase de Transformación y Limpieza...")
        transformer = DataTransformer(raw_data)
        
        df_products = transformer.transform_products()
        df_carts = transformer.transform_carts()
        df_cart_items = transformer.transform_cart_items(df_carts)


        # PASO 3: CARGA (LOAD)
        logging.info("Paso 3: Iniciando fase de Carga en Base de Datos (SQLite)...")
        loader = DataLoader() # se guarda el archivo en data/ecommerce.db
        loader.load_data(df_products, df_carts, df_cart_items)
        
        # MENSAJE DE ÉXITO FINAL
        print("\n" + "="*50)
        print("🎉 PIPELINE ETL EJECUTADO Y CARGADO CON ÉXITO")
        print(f"📦 Productos guardados en SQLite: {len(df_products)}")
        print(f"🛒 Carritos guardados en SQLite: {len(df_carts)}")
        print("📁 Base de datos ubicada en: data/ecommerce.db")
        print("="*50 + "\n")
        
        
        
    except Exception as e:
        logging.error(f"❌ El pipeline falló durante su ejecución: {e}")
        raise

if __name__ == "__main__":
    main()