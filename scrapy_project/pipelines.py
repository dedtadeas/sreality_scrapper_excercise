import psycopg2, os, logging
from itemadapter import ItemAdapter

class FlatsPipeline:
    def __init__(self):
        self.conn = psycopg2.connect(
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=5432,
        )
        
        self.cursor = self.conn.cursor()
        self.logger = logging.getLogger(__name__)
        self.logger.info('db_connection: %s', self.conn)


    def process_item(self, item, spider):
        # Extract the data from the item using ItemAdapter
        adapter = ItemAdapter(item)

        # Define the SQL query to insert data into your database table
        query = f"""
    INSERT INTO {os.getenv('POSTGRES_TABLE')} (title, image_url)
    VALUES (%s, %s)
"""
        # Get the values from the item
        title = adapter.get('title')
        image_url = adapter.get('image_url')
        
        try:
            spider.logger.error(f"Error inserting item into the database:{title}{image_url}")
            # Execute the query with the item's data
            self.cursor.execute(query, (title, image_url))
            # Commit the changes to the database
            self.conn.commit()

        except Exception as e:
            # Handle any exceptions or errors that occur during the database operation
            self.conn.rollback()
            spider.logger.error(f"Error inserting item into the database: {e}")
        
        return item
