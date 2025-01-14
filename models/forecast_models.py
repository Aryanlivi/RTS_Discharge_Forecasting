from sqlalchemy import Column, Float, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from .base import Base, SessionLocal, engine
from datetime import datetime,timezone

# Utility function to get current UTC time
def utc_now():
    return datetime.now(timezone.utc)

class ForecastGalchiToSiurenitar(Base):
    __tablename__ = 'Forecast_Galchi_To_Siurenitar'
    __table_args__ = {'schema': 'public'}
    datetime = Column(DateTime(timezone=True), default=utc_now, primary_key=True)
    discharge = Column(Float)

    __table_args__ = (UniqueConstraint('datetime'),)

class ForecastBudhiToSiurenitar(Base):
    __tablename__ = 'Forecast_Budhi_At_Khari_To_Siurenitar'
    __table_args__ = {'schema': 'public'}
    datetime = Column(DateTime(timezone=True), default=utc_now, primary_key=True)
    discharge = Column(Float)

    __table_args__ = (UniqueConstraint('datetime'),)

class ForecastSiurenitarData(Base):
    __tablename__ = 'Forecast_Siurenitar_Data'
    __table_args__ = {'schema': 'public'}
    datetime = Column(DateTime(timezone=True), default=utc_now, primary_key=True)
    discharge = Column(Float)

    __table_args__ = (UniqueConstraint('datetime'),)
