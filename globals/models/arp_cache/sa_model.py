from sqlalchemy import Table, Column, Integer, Boolean, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from models.base import Base

class ARPCache(Base):
    __tablename__ = 'arp_cache'
    id  = Column(Integer, primary_key=True) 
    mac = Column(String(32), nullable=False, unique=True)
    ip  = Column(String(32), default='')


