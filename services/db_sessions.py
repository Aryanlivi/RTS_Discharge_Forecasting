from sqlalchemy.orm import Session
from models.base import SessionLocal,Base,engine
from models.forecast_models import ForecastGalchiToSiurenitar, ForecastBudhiToSiurenitar, ForecastSiurenitarData
import logging
from datetime import datetime,timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Create all tables
def create_tables():
    try:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        print("All tables created successfully.")
    except Exception as e:
        print(f"Error during table creation: {e}")


# Dependency to get DB session
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility class for database operations
class Database:
    def __init__(self):
        self.session = SessionLocal()
        

    def insert_or_update(self, model, data):
        try:
            existing = self.session.query(model).filter_by(datetime=data['datetime']).first()
            if existing:
                for key, value in data.items():
                    setattr(existing, key, value)
            else:
                new_entry = model(**data)
                self.session.add(new_entry)

            self.session.commit()
            logger.info(f"Data inserted/updated successfully in {model.__tablename__}: {data}")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error inserting/updating data in {model.__tablename__}: {e}")
        finally:
            self.session.close()

    def fetch_latest_discharge(self, model, datetime):
        try:
            result = (
                self.session.query(model)
                .filter(model.datetime <= datetime)
                .order_by(model.datetime.desc())
                .first()
            )
            return result.discharge if result else None
        except Exception as e:
            logger.error(f"Error fetching latest discharge from {model.__tablename__}: {e}")
            return None
        finally:
            self.session.close()
            
    def get_row_by_datetime(self, model, datetime_value):
        try:
            # Query the database for the row with the specific datetime
            result = self.session.query(model).filter_by(datetime=datetime_value).first()
            
            if result:
                logger.info(f"Row found for {model.__tablename__} with datetime: {datetime_value}")
                # Convert the datetime to UTC if it's not already in UTC
                datetime_str = result.datetime.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S') if result.datetime else None
                return {
                    'datetime': datetime_str,
                    'discharge': result.discharge
                }
            else:
                logger.info(f"No row found for {model.__tablename__} with datetime: {datetime_value}")
                return None
        except Exception as e:
            logger.error(f"Error retrieving row for {model.__tablename__} with datetime {datetime_value}: {e}")
            return None
        finally:
            self.session.close()


    