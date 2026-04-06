import os
import pyodbc
from dotenv import load_dotenv


load_dotenv()

def get_db_connection():
    """Çevre değişkenlerini kullanarak veritabanı bağlantısı oluşturur."""
    server = os.environ.get("DBSERVER")
    database = os.environ.get("DBNAME")
    username = os.environ.get("DBUSERNAME")
    password = os.environ.get("DBPASSWORD")
    driver = os.environ.get("DBDRIVER")
    
    
    conn_str = (
        f'DRIVER={driver};'
        f'SERVER={server};'
        f'PORT=1433;'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )
    return pyodbc.connect(conn_str)

def main():
    try:
        with get_db_connection() as cnxn:
            cursor = cnxn.cursor()

            print("--- İlk Ürün Bilgisi Çekiliyor ---")
            cursor.execute("SELECT TOP 1 * FROM [SalesLT].[Product]")
            row = cursor.fetchone()
            if row:
                print(f"İlk Kayıt: {row}")

            print("\n--- Kategori ve Ürün JOIN Sorgusu (İlk 20) ---")
            query = """
                SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName 
                FROM [SalesLT].[ProductCategory] pc 
                JOIN [SalesLT].[Product] p ON pc.productcategoryid = p.productcategoryid
            """
            cursor.execute(query)
            
            row = cursor.fetchone()
            while row:
                print(f"Kategori: {row[0]} | Ürün: {row[1]}")
                row = cursor.fetchone()

    except pyodbc.Error as e:
        print(f"Veritabanı bağlantı hatası oluştu: {e}")
    except Exception as ex:
        print(f"Beklenmedik bir hata oluştu: {ex}")

if __name__ == "__main__":
    main()
