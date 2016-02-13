from sqlalchemy import Table, Column, Integer, Boolean, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from models.base import Base

class InetEther(Base):
    __tablename__ = 'inet_ether'
    id  = Column(Integer, primary_key=True) 
    mac = Column(String(32), nullable=False, unique=True)
    ip  = Column(String(32), default='')
    access_type = Column(String(8), default='')
    lastupdate = Column(DateTime(timezone=False), default=func.now())
    is_active = Column(Boolean, default=True)


