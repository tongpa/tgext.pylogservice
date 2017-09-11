# -*- coding: utf-8 -*-
#from sqlalchemy.sql import func; 
from sqlalchemy import  Column
from sqlalchemy.types import   DateTime, Integer, String, Text
from sqlalchemy.sql import func

from sqlalchemy.dialects.mysql import BIT
#from pollandsurvey.model import DeclarativeBase, metadata, DBSession
from sqlalchemy.ext.declarative import declarative_base
from tgext.pylogservice.models import DeclarativeBase, metadata, DBSession
__all__ = ['LogSurvey']

class LogSurvey(DeclarativeBase):
    __tablename__ = 'sur_log_survey'

    id_log_survey =  Column(Integer, autoincrement=True, primary_key=True);
    ip_server = Column(String(20), nullable=True);
    ip_client = Column(String(20), nullable=True);
    #status  = Column(String(20), nullable=True);
    
    relative_created  = Column(String(20), nullable=True);
    name = Column(String(255), nullable=True);
    log_level = Column(String(20), nullable=True);
    level_text = Column(String(20), nullable=True);
    message = Column(Text, nullable=True);
    file_name = Column(String(255), nullable=True);
    path_name = Column(Text, nullable=True);
    line_no = Column(String(10), nullable=True);
    milliseconds = Column(String(20), nullable=True);
    exception = Column(Text, nullable=True);
    thread = Column(String(10), nullable=True);
    
    current_page = Column(String(255), nullable=True);
    user_name = Column(String(255), nullable=True);
    active  = Column(BIT, nullable=True, default=1);
    create_date = Column(DateTime, default=func.now());
    
    modules = Column(String(255), nullable=True);
    #update_date = Column(DateTime ,onupdate=sql.func.utc_timestamp());
    
    def __init__(self):
        self.active = 1;       
        
     
    def __unicode__(self):
        return self.__repr__()    
        
    def __repr__(self):
        return "<Log: %s - %s>" % (self.create_date.strftime('%m/%d/%Y-%H:%M:%S'), self.message[:50])
    
    def save(self):
        DBSession.add(self) 
        DBSession.flush()
    