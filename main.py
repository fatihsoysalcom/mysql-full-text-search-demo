import mysql.connector
from mysql.connector import Error

# Database configuration - IMPORTANT: CHANGE THE PASSWORD FOR YOUR SETUP
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_mysql_root_password', # <--- CHANGE THIS to your MySQL root password
    'database': 'fulltext_demo'
}

def create_database_and_table(cursor):
    """Creates the database and the 'articles' table with a FULLTEXT index."""
    try:
        # Drop database if it exists to ensure a clean start
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_CONFIG['database']}")
        print(f"Database '{DB_CONFIG['database']}' dropped if it existed.")

        # Create the database with UTF8MB4 support for Turkish characters
        cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"Database '{DB_CONFIG['database']}' created.")
        cursor.execute(f"USE {DB_CONFIG['database']}")

        # Create articles table with a FULLTEXT index on the 'content' column
        create_table_query = """
        CREATE TABLE articles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            -- This is where the Full-Text Index is defined
            FULLTEXT (content)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        cursor.execute(create_table_query)
        print("Table 'articles' created with FULLTEXT index on 'content'.")

    except Error as e:
        print(f"Error during database/table creation: {e}")
        raise

def insert_sample_data(cursor):
    """Inserts sample Turkish article data into the 'articles' table."""
    articles_data = [
        ("MySQL Full-Text Search", "MySQL'de tam metin arama, büyük veri kümelerinde hızlı ve etkili arama yapmayı sağlar. Geleneksel LIKE operatörüne göre çok daha performanslıdır."),
        ("Veritabanı Optimizasyonu", "Veritabanı performansını artırmak için indeksleme ve sorgu optimizasyonu kritik öneme sahiptir. Full-Text Search, metin tabanlı aramaları optimize eder."),
        ("Web Uygulamaları ve Arama", "Modern web uygulamaları, kullanıcıların aradıkları bilgiye anında ulaşmasını bekler. Tam metin arama motorları bu beklentiyi karşılar."),
        ("Ubuntu ve MySQL Kurulumu", "Ubuntu 16.04 üzerinde MySQL 5.6 kurulumu ve yapılandırması, sunucu tarafında önemli bir adımdır. Güvenlik ayarları unutulmamalıdır."),
        ("SQL ve Performans", "SQL sorgularında performans, veritabanı tasarımından ve indeks kullanımından büyük ölçüde etkilenir. Tam metin indeksleri, metin aramalarını hızlandırır.")
    ]
    insert_query = "INSERT INTO articles (title, content) VALUES (%s, %s)"
    cursor.executemany(insert_query, articles_data)
    print(f"{len(articles_data)} sample articles inserted.")

def run_searches(cursor):
    """Demonstrates traditional LIKE and Full-Text Search queries."""
    print("\n--- Demonstrating Search Queries ---")

    # 1. Traditional LIKE search (as discussed in the article for comparison)
    print("\n1. Traditional LIKE search for 'veritabanı':")
    like_query = "SELECT id, title FROM articles WHERE content LIKE '%veritabanı%';"
    cursor.execute(like_query)
    for (id, title) in cursor:
        print(f"  ID: {id}, Title: {title}")
    print(f"  Found {cursor.rowcount} results with LIKE.")

    # 2. Full-Text Search - NATURAL LANGUAGE MODE
    # This is the primary feature demonstrated by the article.
    print("\n2. Full-Text Search (NATURAL LANGUAGE MODE) for 'arama performans':")
    # The MATCH() function specifies the columns to search, and AGAINST() specifies the search string.
    # NATURAL LANGUAGE MODE is the default if no mode is specified, but explicitly stated here.
    fts_natural_query = """
    SELECT id, title, content,
           MATCH(content) AGAINST('arama performans' IN NATURAL LANGUAGE MODE) AS score
    FROM articles
    WHERE MATCH(content) AGAINST('arama performans' IN NATURAL LANGUAGE MODE)
    ORDER BY score DESC;
    """
    cursor.execute(fts_natural_query)
    for (id, title, content, score) in cursor:
        print(f"  ID: {id}, Title: {title}, Score: {score:.2f}")
    print(f"  Found {cursor.rowcount} results with FTS Natural Language Mode.")

    # 3. Full-Text Search - BOOLEAN MODE
    # Demonstrates more advanced search capabilities like required words (+), excluded words (-), etc.
    print("\n3. Full-Text Search (BOOLEAN MODE) for '+mysql -ubuntu':")
    # '+mysql' means 'mysql' must be present. '-ubuntu' means 'ubuntu' must NOT be present.
    fts_boolean_query = """
    SELECT id, title, content,
           MATCH(content) AGAINST('+mysql -ubuntu' IN BOOLEAN MODE) AS score
    FROM articles
    WHERE MATCH(content) AGAINST('+mysql -ubuntu' IN BOOLEAN MODE)
    ORDER BY score DESC;
    """
    cursor.execute(fts_boolean_query)
    for (id, title, content, score) in cursor:
        print(f"  ID: {id}, Title: {title}, Score: {score:.2f}")
    print(f"  Found {cursor.rowcount} results with FTS Boolean Mode.")

def cleanup(cursor):
    """Drops the created database."""
    try:
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_CONFIG['database']}")
        print(f"\nDatabase '{DB_CONFIG['database']}' dropped.")
    except Error as e:
        print(f"Error during cleanup: {e}")

def main():
    conn = None
    try:
        # Connect to MySQL server without specifying a database initially to create it
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        if conn.is_connected():
            cursor = conn.cursor()
            print("Successfully connected to MySQL server.")

            create_database_and_table(cursor)
            insert_sample_data(cursor)
            conn.commit() # Commit changes after creating table and inserting data

            run_searches(cursor)

    except Error as e:
        print(f"Failed to connect to MySQL or encountered a database error: {e}")
        print("Please ensure MySQL is running and credentials in DB_CONFIG are correct.")
        print("You might need to install mysql-connector-python: pip install mysql-connector-python")
    finally:
        if conn and conn.is_connected():
            # Perform cleanup before closing connection
            if 'cursor' in locals(): # Ensure cursor was created before attempting to use it
                cleanup(cursor)
                conn.commit() # Commit cleanup changes
                cursor.close()
            conn.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    main()
