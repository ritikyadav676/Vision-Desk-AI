import mysql.connector
 
 
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",
    "database": "visiondesk_ai"
}
 
 
def get_connection():
    """
    Create and return a MySQL database connection.
    """
 
    connection = mysql.connector.connect(**DB_CONFIG)
 
    return connection
 
 
def test_connection():
    """
    Test whether MySQL connection is working.
    """
 
    connection = get_connection()
 
    if connection.is_connected():
        print("MySQL connected successfully!")
 
    connection.close()
 
 
def insert_chunk(
    filename,
    file_type,
    document_type,
    page_number,
    chunk_id,
    content
):
    """
    Insert one document chunk into MySQL.
    """
 
    connection = get_connection()
    cursor = connection.cursor()
 
    query = """
        INSERT INTO document_chunks
        (
            filename,
            file_type,
            document_type,
            page_number,
            chunk_id,
            content
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """
 
    values = (
        filename,
        file_type,
        document_type,
        page_number,
        chunk_id,
        content
    )
 
    cursor.execute(query, values)
 
    connection.commit()
 
    cursor.close()
    connection.close()
 
    print("Chunk inserted successfully!")
 
 
def search_documents(keyword):
    """
    Search document chunks using a keyword.
    """
 
    connection = get_connection()
 
    cursor = connection.cursor(dictionary=True)
 
    query = """
        SELECT
            filename,
            file_type,
            document_type,
            page_number,
            chunk_id,
            content
        FROM document_chunks
        WHERE content LIKE %s
    """
 
    search_value = f"%{keyword}%"
 
    cursor.execute(query, (search_value,))
 
    results = cursor.fetchall()
 
    cursor.close()
    connection.close()
 
    return results