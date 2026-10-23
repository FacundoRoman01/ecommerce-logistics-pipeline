import logging
from src.extract import DataExtractor
from src.transform import DataTransformer

# Configuración de los logs principales del orquestador
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    """
    Función principal que coordina el flujo completo del pipeline de datos:
    Extracción -> Transformación -> (Próximamente Carga)
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
        
        # MOSTRAR RESULTADOS FINALES EN CONSOLA
        print("\n" + "="*50)
        print("🎉 PIPELINE EJECUTADO CON ÉXITO")
        print(f"📦 Total de productos limpios listos para cargar: {len(df_products)}")
        print(f"🛒 Total de órdenes/carritos listos para cargar: {len(df_carts)}")
        print("="*50 + "\n")
        
        # (Acá en el futuro agregaremos el Paso 3: LOAD / Carga a SQLite)
        
    except Exception as e:
        logging.error(f"❌ El pipeline falló durante su ejecución: {e}")
        raise

if __name__ == "__main__":
    main()