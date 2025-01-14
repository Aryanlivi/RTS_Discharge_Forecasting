import psycopg2
import sys
import os

# Add the parent directory to the system path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from DB_Service.Loggers import *
from datetime import datetime

load_dotenv()

SERVER=os.getenv('server')
USERNAME=os.getenv('username')
PASSWORD=os.getenv('password')
DATABASE=os.getenv('database')



logger=Logger().get_logger()
class Database:
    def __init__(self):
        self.cursor=None
        self.connection=None   
    def connect(self):
        try:
            self.connection=psycopg2.connect(
                host=SERVER,
                database=DATABASE,
                user=USERNAME,
                password=PASSWORD
            )
            logger.info("Database connection established successfully.")
            return self.connection 
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}")
            return None
    def execute_query(self, query):
        if self.connection:
            try:
                self.cursor = self.connection.cursor()
                self.cursor.execute(query)
                self.connection.commit()
                logger.info(f"Query executed successfully: {query}")
            except Exception as e:
                self.connection.rollback()  # Rollback on error
                logger.error(f"Error executing query '{query}': {e}")
            finally:
                self.cursor.close()


    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed.")
        
    def fetch(self, query):
        try:
            if self.connection:
                self.cursor = self.connection.cursor()
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                logger.info(f"Data fetched successfully for query: {query}")
                return result
        except Exception as e:
            logger.error(f"Error fetching data for query '{query}': {e}")
            return None
        finally:
            if self.cursor:
                self.cursor.close()

        
    def insert_data(self, table, data):
        if self.connection:
            try:
                columns = ', '.join(data.keys())
                values = tuple(data.values())
                update_clause = ', '.join([f"{col} = EXCLUDED.{col}" for col in data.keys()])

                query = f"""
                INSERT INTO {table} ({columns}) 
                VALUES ({', '.join(['%s'] * len(values))})
                ON CONFLICT (dateTime) DO UPDATE SET {update_clause};
                """

                self.cursor = self.connection.cursor()
                self.cursor.execute(query, values)
                self.connection.commit()
                logger.info(f"Data inserted/updated successfully into {table}: {data}")
            except Exception as e:
                self.connection.rollback()  # Rollback on error
                logger.error(f"Error inserting data into {table}: {data} - {e}")
            finally:
                self.cursor.close() 