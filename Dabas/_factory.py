from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import logging 
Logger= logging.Logger(__name__)



class SessionFactory:
    
    def __init__(self, db_name, 
                 username=None, password=None, host='localhost', port=None, 
                 echo=False, pool_size=10, max_overflow=20):
        
        
        
        self.db_name = db_name
        self.username = username or ""
        self.password = password or ""
        self.host = host
        self.port = port
        self.echo = echo
        self.pool_size = pool_size
        self.max_overflow = max_overflow

    def _create_session(self, dialect_driver:str, default_port=None):
        """General method to create URL and session"""
        try:
            port = self.port or default_port
            
            url = f"{dialect_driver}://{self.username}:{self.password}@{self.host}:{port}/{self.db_name}"
            engine = create_engine(url, echo=self.echo, pool_size=self.pool_size, max_overflow=self.max_overflow)
            
            return sessionmaker(bind=engine, expire_on_commit=False)
        except Exception as e:
            
            Logger.error(f"Error connecting to {dialect_driver}: {e}")

            return None
    
    def sqlite(self):
        """Create URL and session for SQLite"""
        try:
            
            url = f"sqlite:///{self.db_name}"
           
            engine = create_engine(url, echo=self.echo)  # without port and pool_size
            
            return sessionmaker(bind=engine, expire_on_commit=False)
        
        except Exception as e:
            
            Logger.error(f"Error connecting to sqlite: {e}")

            return None
    


    def postgresql(self):
        return self._create_session("postgresql", default_port=5432)

    def mysql(self):
        return self._create_session("mysql+pymysql", default_port=3306)

    def mariadb(self):
        return self._create_session("mariadb+pymysql", default_port=3306)

    def mssql(self):
        return self._create_session("mssql+pymssql", default_port=1433)

    def oracle(self):
        return self._create_session("oracle", default_port=1521)

    def db2(self):
        return self._create_session("ibm_db", default_port=50000)

    def firebird(self):
        return self._create_session("firebird", default_port=3050)





    