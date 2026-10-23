import requests
import logging

# Configuración de los logs para ver mensajes informativos 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class DataExtractor:
    #constructor
    def __init__(self):
        # Definimos la URL base de la API 
        self.base_url = "https://fakestoreapi.com"

    def fetch_data(self, endpoint: str):
        """
        Método para hacer una petición GET a un endpoint específico de la API.
        """
        url = f"{self.base_url}/{endpoint}"
        
        # Avisamos por los logs que estamos intentando extraer
        logging.info(f"Iniciando extracción desde el endpoint: {endpoint}")
        
        # Hacemos la petición HTTP a la web usando requests
        response = requests.get(url, timeout=10)
        
        # Convertimos la respuesta de texto plano/JSON a un formato que Python entienda 
        data = response.json()
        
        logging.info(f"Extracción exitosa de {endpoint}. Registros obtenidos: {len(data)}")
        return data



    def extract_ecommerce_data(self):
        """
        Método principal que coordina la extracción de productos y órdenes (carritos).
        """
        try:
            products = self.fetch_data("products")
            carts = self.fetch_data("carts")
            
            # Devolvemos un diccionario con ambos datasets listos para transformar
            return {
                "products": products,
                "carts": carts
            }
        except Exception as e:
            logging.error(f"Error crítico en el proceso de extracción: {e}")
            raise

# Bloque de prueba local: si ejecutamos este archivo directamente, se prueba la extracción
if __name__ == "__main__":
    extractor = DataExtractor()
    data = extractor.extract_ecommerce_data()
    
    print("\n--- PRUEBA DE EXTRACCIÓN EXITOSA ---")
    print(f"Productos extraídos: {len(data['products'])}")
    print(f"Carritos/Órdenes extraídos: {len(data['carts'])}")