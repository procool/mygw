from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func

class Users(object):
    __tablename__ = 'users'
    id  = Column(Integer, primary_key=True) 
    login  = Column(String(32), default=False)
    passwd = Column(String(128), nullable=True)
    status = Column(Integer)
    is_active = Column(Boolean, default=True)
    lastupdate = Column(DateTime(timezone=False), default=func.now())
    crdate = Column(DateTime(timezone=False), default=func.now())




