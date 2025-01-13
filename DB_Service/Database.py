import psycopg2
import os
from dotenv import load_dotenv
from .Loggers import *
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
            print("Connected DB Successfully")
            return self.connection 
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}")
            return None
    def execute_query(self,query):
        if self.connection:
            try:
                self.cursor = self.connection.cursor()
                self.cursor.execute(query)
                self.connection.commit()
                logger.info(f"Query executed successfully: {query}")
                self.cursor.close()
            except Exception as e:
                logger.error(f"Error executing query '{query}': {e}")

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed.")
        
    def fetch(self,query):
        try:
            if self.connection:
                self.cursor = self.connection.cursor()
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                logger.info(f"Data fetched successfully for query: {query}")
                self.cursor.close()
                logger.info(f"Fetched Data:{result}")
                return result
        except Exception as e:
            logger.error(f"Error fetching data for query '{query}': {e}")
            return None 
        
    def insert_data(self, table, data):
        if self.connection:
            try:
                # Prepare the columns and values for the query dynamically
                columns = ', '.join(data.keys())
                values = tuple(data.values())
                
                # Create the dynamic INSERT SQL statement
                query = f"""
                INSERT INTO {table} ({columns}) 
                VALUES ({', '.join(['%s'] * len(values))})
                """
                
                # Execute the query
                self.cursor = self.connection.cursor()
                self.cursor.execute(query, values)
                self.connection.commit()
                logger.info(f"Data inserted successfully into {table}: {data}")
                self.cursor.close()
            except Exception as e:
                logger.error(f"Error inserting data into {table}: {data} - {e}")
                return None
