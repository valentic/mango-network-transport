###########################################################################
#
#   Mango Data Models
#
#   Needs postgresql postgresql-server sqlalchemy
#
#   2021-08-01  Todd Valentic
#               Initial implementation.
#
###########################################################################

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, ForeignKey, func, Index
from sqlalchemy import ForeignKeyConstraint, UniqueConstraint
from sqlalchemy import DateTime, String, BigInteger, Integer, Float, Boolean, Numeric
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects import postgresql

database = 'postgresql://@/mango'
session = scoped_session(sessionmaker())

Base = declarative_base()
Base.query = session.query_property()
Base.metadata.bind = create_engine(database)

#-- Utility functions --------------------------------------------

def create():
    Base.metadata.create_all()

def add(entry):
    session.add(entry)

def delete(entry):
    session.delete(entry)

def save(entry):
    session.add(entry)

def merge(entry):
    return session.merge(entry)

def commit():
    session.commit()

def rollback():
    session.rollback()

def remove():
    session.remove()

#------------------------------------------------------------------------------
# Stations
#------------------------------------------------------------------------------

class Station(Base):

    __tablename__ = 'station'

    id          = Column(Integer, primary_key=True)
    name        = Column(String, unique=True)
    label       = Column(String)
    model_id    = Column(Integer, ForeignKey('system_model.id'))
    status_id   = Column(Integer, ForeignKey('status.id'))

    def __repr__(self):
        return '<Station %s (%s)>' % \
            (self.name,self.id)

class Status(Base):

    __tablename__ = 'status'

    id      = Column(Integer, primary_key=True)
    name    = Column(String, unique=True)
    label   = Column(String)

    def __repr__(self):
        return '<Status %s (%s)>' % \
            (self.name,self.id)

class SystemModel(Base):

    __tablename__ = 'system_model'

    id      = Column(Integer, primary_key=True)
    name    = Column(String, unique=True)
    label   = Column(String)

    def __repr__(self):
        return '<SystemModel %s (%s)>' % \
            (self.name,self.id)

class Device(Base):

    __tablename__ = 'device'

    id      = Column(Integer, primary_key=True)
    name    = Column(String, unique=True)
    label   = Column(String)

    def __repr__(self):
        return '<Device %s (%s)>' % \
            (self.name,self.id)

class Instrument(Base):

    __tablename__ = 'instrument'

    id          = Column(Integer, primary_key=True)
    name        = Column(String, unique=True)
    label       = Column(String)

    def __repr__(self):
        return '<Instrument %s (%s)>' % \
            (self.name,self.id)

class StationInstrument(Base):
    
    __tablename__ = 'stationinstrument'

    id              = Column(Integer, primary_key=True)
    station_id      = Column(Integer, ForeignKey('station.id'))
    instrument_id   = Column(Integer, ForeignKey('instrument.id'))

    def __repr__(self):
        return '<StationInstrument %s (station %s, instrument %s)>' % \
            (self.id, self.station_id, self.instrument_id)

#------------------------------------------------------------------------------
# Images 
#------------------------------------------------------------------------------

class Image(Base):

    __tablename__ = 'image'


    id              = Column(Integer, primary_key=True)
    timestamp       = Column(DateTime(timezone=True))
    device_id       = Column(Integer, ForeignKey('device.id'))
    serialnum       = Column(Integer)

    latitude        = Column(Float)
    longitude       = Column(Float)
    exposure_time   = Column(Float)
    ccd_temp        = Column(Float)
    set_point       = Column(Float)
    image_bytes     = Column(Integer)
    x               = Column(Integer)
    y               = Column(Integer)
    width           = Column(Integer)
    height          = Column(Integer)
    bin_x           = Column(Integer)
    bin_y           = Column(Integer)

    stationinstrument_id = Column(Integer, ForeignKey('stationinstrument.id'))

    __table_args__ = (
        Index('stationinstrument_id_timestamp_idx',stationinstrument_id,timestamp),    
    )

    def __repr__(self):
        return '<Image %s %s>' % \
            (self.timestamp,self.stationinstrument_id)
