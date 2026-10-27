import sqlite3
import pandas as pd
import logging
import os

# Configurar logs correctamente
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def obtener_reporte_ventas_detalladas(connection):
    """Vista detallada de cada ítem vendido (JOIN completo)."""
    query = """
    SELECT 
        c.id AS cart_id,
        c.userId,
        c.date AS cart_date,
        p.title AS product_title,
        p.category,
        ci.quantity,
        p.price,
        ROUND(ci.quantity * p.price, 2) AS total_item_price
    FROM carts c
    JOIN cart_items ci ON c.id = ci.cart_id
    JOIN products p ON ci.product_id = p.id;
    """
    return pd.read_sql_query(query, connection)

def obtener_top_productos(connection):
    """Agrupa por producto para saber cuáles se venden más y cuánto facturan."""
    query = """
    SELECT 
        p.title AS product_title,
        p.category,
        SUM(ci.quantity) AS total_units_sold,
        ROUND(SUM(ci.quantity * p.price), 2) AS total_revenue
    FROM cart_items ci
    JOIN products p ON ci.product_id = p.id
    GROUP BY p.id, p.title, p.category
    ORDER BY total_units_sold DESC;
    """
    return pd.read_sql_query(query, connection)

def obtener_ventas_por_usuario(connection):
    """Muestra el comportamiento de compra por cada usuario."""
    query = """
    SELECT 
        c.userId,
        COUNT(DISTINCT c.id) AS total_carts,
        SUM(ci.quantity) AS total_items_bought,
        ROUND(SUM(ci.quantity * p.price), 2) AS total_spent
    FROM carts c
    JOIN cart_items ci ON c.id = ci.cart_id
    JOIN products p ON ci.product_id = p.id
    GROUP BY c.userId
    ORDER BY total_spent DESC;
    """
    return pd.read_sql_query(query, connection)

def obtener_ventas_por_categoria(connection):
    """Agrupa las ventas totales según la categoría del producto."""
    query = """
    SELECT 
        p.category,
        SUM(ci.quantity) AS units_sold,
        ROUND(SUM(ci.quantity * p.price), 2) AS category_revenue
    FROM cart_items ci
    JOIN products p ON ci.product_id = p.id
    GROUP BY p.category
    ORDER BY category_revenue DESC;
    """
    return pd.read_sql_query(query, connection)

def exportar_reporte_excel():
    db_path = "data/ecommerce.db"
    output_excel = "data/ecommerce_report.xlsx"
    
    # Asegurarnos de que la carpeta data exista
    os.makedirs(os.path.dirname(output_excel), exist_ok=True)
    
    logging.info("🔌 Conectando a la base de datos SQLite para extraer métricas...")
    with sqlite3.connect(db_path) as conn:
        
        # Obtenemos los DataFrames de cada consulta
        df_ventas = obtener_reporte_ventas_detalladas(conn)
        df_top_prod = obtener_top_productos(conn)
        df_usuarios = obtener_ventas_por_usuario(conn)
        df_categorias = obtener_ventas_por_categoria(conn)
        
    logging.info(f"📊 Exportando reportes a Excel multipestaña: {output_excel}")
    
    # Usamos Pandas ExcelWriter con el motor 'openpyxl' para guardar cada DataFrame en una pestaña distinta
    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        df_ventas.to_excel(writer, sheet_name='Detalle_Ventas', index=False)
        df_top_prod.to_excel(writer, sheet_name='Top_Productos', index=False)
        df_usuarios.to_excel(writer, sheet_name='Ventas_Usuarios', index=False)
        df_categorias.to_excel(writer, sheet_name='Ventas_Categorias', index=False)
        
    logging.info("🎉 ¡Reporte Excel multipestaña generado y guardado con éxito!")

if __name__ == "__main__":
    exportar_reporte_excel()