import sys, string, time, logging

from sqlalchemy import create_engine; 
from datetime import datetime;

from tg.configuration import AppConfig, config
from .models import LogSurvey, DeclarativeBase, init_model, DBSession
import socket;
from datetime import datetime, timedelta
class LogDBHandler(logging.Handler):
    
    def __init__(self,  config,request):
        logging.Handler.__init__(self)
        
        
        self.sqlConfig = config['sqlalchemy.url'] ;
         
         
        self.engine = create_engine(self.sqlConfig);  
        
        init_model(self.engine)
        
        self.request =  request;
        self.ipserver = socket.gethostbyname(socket.gethostname());
        
         
         
    
    def __setSQL__(self):
        return  """ INSERT INTO sur_log_survey(ip_server, ip_client, relative_created, name, log_level, level_text,message, file_name,
                    path_name, line_no, milliseconds, exception, thread, user_name, current_page, create_date
        ) VALUES(
                    '""" + str(self.ipserver) + """',
                    '""" + str(self.ipclient) + """',
                    %(relativeCreated)d,
                    "%(name)s",
                    %(levelno)d,
                    "%(levelname)s",
                    "%(message)s",
                    "%(filename)s",
                    "%(pathname)s",
                    %(lineno)d,
                    %(msecs)d,
                    "%(exc_text)s",
                    "%(thread)s",
                    \"""" +  str(self.user) + """\",'','"""+ str(datetime.now()) + """'    ); """;
                    
    def __setSQL1__(self):
        return  """ INSERT INTO sur_log_survey(
                    ip_server,
                    ip_client,
                    relative_created,
                    name,
                    log_level,
                    level_text,
                    message,
                    file_name,
                    path_name,
                    line_no,
                    milliseconds,
                    exception,
                    thread,
                    user_name,
                    current_page,
                    create_date
        ) VALUES(
                    '""" + str(self.ipserver) + """',
                    '""" + str(self.ipclient) + """',
                    "%(relativeCreated)",
                    "%(name)",
                    "%(levelno)",
                    "%(levelname)",
                    "%(message)",
                    "%(filename)",
                    "%(pathname)",
                    "%(lineno)",
                    "%(msecs)",
                    "%(exc_text)",
                    "%(thread)",
                    \"""" +  str(self.user) + """\",'','"""+ str(datetime.now()) + """'    ); """;
    
    def formatDBTime(self, record):
        record.dbtime = time.strftime("#%m/%d/%Y#", time.localtime(record.created))

    def emit(self,record):
       
         
        try: 
            #use default formatting
            self.format(record)
            #now set the database time up
            self.formatDBTime(record)
            if record.exc_info:
                record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
            else:
                record.exc_text = ""
            
            print self.request
            
            self.user =  "GUEST";
            
            if(self.request and self.request.identity is not None) : #and self.request.identity is not None
                self.user =  self.request.identity['user'];
            
                
                
            
            if 'HTTP_X_FORWARDED_FOR' in self.request.environ :
                self.ipclient = self.request.environ['HTTP_X_FORWARDED_FOR']; 
            else:
                self.ipclient = self.request.remote_addr;
            
            
            
            log = LogSurvey()
            log.ip_server = str(self.ipserver) 
            log.ip_client = str(self.ipclient)
            
            log.relative_created  = record.__dict__['relativeCreated'] #timedelta(seconds=record.__dict__['relativeCreated']) 
            log.name = record.__dict__['name']
            log.log_level = record.__dict__['levelno']
            log.level_text = record.__dict__['levelname']
            log.message = record.__dict__['msg']
            log.file_name = record.__dict__['filename']
            log.path_name = record.__dict__['pathname']
            log.line_no = record.__dict__['lineno']
            log.milliseconds = record.__dict__['msecs']#timedelta(seconds=record.__dict__['msecs'])  
            log.exception = record.__dict__['exc_text']
            log.thread = record.__dict__['thread']
            
            #log.current_page = record.__dict__[]
            log.user_name = str(self.user)
            #log.active  = record.__dict__[]
            log.create_date = str(datetime.now())
            
            DBSession.add(log) 
        except:
            import traceback
            ei = sys.exc_info()
            traceback.print_exception(ei[0], ei[1], ei[2], None, sys.stderr)
            del ei
            
    def emit_old(self, record):
        try:
            
            #use default formatting
            self.format(record)
            #now set the database time up
            self.formatDBTime(record)
            if record.exc_info:
                record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
            else:
                record.exc_text = ""
            
            record.message =  record.message.replace("\"", "'");
            
            if(self.request and self.request.identity):
                self.user =  self.request.identity['user'];
            else:
                self.user =  "GUEST";
            
            if 'HTTP_X_FORWARDED_FOR' in self.request.environ :
                self.ipclient = self.request.environ['HTTP_X_FORWARDED_FOR'];
            else:
                self.ipclient = self.request.remote_addr;
                
            #self.ipclient = self.request.environ['HTTP_X_FORWARDED_FOR'] ;#self.request.environ['COMPUTERNAME'] +'-' + self.request.remote_addr;#self.request.remote_user ;#self.request.remote_addr;
            
            self.SQL = self.__setSQL__();    
            
            dicts = record.__dict__;
            
            #for u in dicts:
            #    print "%s  %s", (   u,  dicts[u]) ;
            
            
            
            sql = self.SQL % record.__dict__
            
            #print sql; 
            
            conn = self.engine.connect();
            
            conn.execute(sql);
             
             
        except:
            import traceback
            ei = sys.exc_info()
            traceback.print_exception(ei[0], ei[1], ei[2], None, sys.stderr)
            del ei

    def close(self):
         
        logging.Handler.close(self)
        

