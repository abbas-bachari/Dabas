from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy import Engine, or_, and_
from typing import List, Dict,Any
from ._data import Data
from sqlalchemy.ext import  ColumnExpressionArgument


class DatabaseManager:
    def __init__(self, engine: Engine, base):
        """Initialize the database manager with a session factory."""
        self.engine = engine
        self.base = base  # دریافت کلاس‌های مدل (Base)
        self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)
    
    def create_tables(self):
        """Create tables if they don't exist"""
        try:
            self.base.metadata.create_all(self.engine)
            return True
        except SQLAlchemyError as e:
            print(f"❌ Error creating tables: {e._message()}")

    def execute_transaction(self, operation, *args, **kwargs):
        """Automatically manages database transactions.
        
        ## Usage:
        ```
            def operation(session):
                session.add(model_instance)
                return True

            result= execute_transaction(operation)
        ```
        
        """
        with self.session_factory() as session:
            try:
                result = operation(session, *args, **kwargs)
                session.commit()
                return result
            except SQLAlchemyError as e:
                session.rollback()
                print(f"❌ Error Transaction: {e._message()}")
                # For example, you can return None, False or raise an exception
                return None
    
    def insert(self, model_instance) -> bool:
        """Add a new record to the database."""
        def operation(session:Session):
            
            session.add(model_instance)
            
            return True

        result=self.execute_transaction(operation) 
        return result or False
    
    def get(self, model_class,limit=None,conditions:list=None, order_by=None,descending=False )->List:
        

        """
        Retrieve data based on SQLAlchemy filter conditions.

        Args:
            model_class (type): The SQLAlchemy model class to retrieve from.
            conditions (List, optional): A list of SQLAlchemy filter conditions. Defaults to None.
            limit (int, optional): The number of records per page. Defaults to None.
            order_by (str, optional): The column name for ordering results. Defaults to None.
            descending (bool, optional): If True, sorts in descending order. Defaults to False.

        Returns:
            List: A list of records retrieved from the database.

        ### Example usage of different conditions:

            conditions=[]
            conditions.append(model_class.column_name == 'value')
            conditions.append(model_class.column_name != 'value')
            conditions.append(model_class.column_name.in_(['value', 'value2']))
            conditions.append(model_class.column_name.like('%value%'))
            conditions.append(model_class.column_name.ilike('%value%'))
            conditions.append(model_class.column_name.is_(None))
            conditions.append(model_class.column_name.isnot(None))
            conditions.append(model_class.column_name.between(1, 10))
            conditions.append(model_class.column_name.notbetween(1, 10))
        """
        
        def operation(session:Session):
            query = session.query(model_class)
            
            # Apply filters
            if conditions:
                query = query.filter(and_(*conditions))

            
            
            # Apply ordering
            if order_by:
                order_column = getattr(model_class, order_by)
                query = query.order_by(order_column.desc() if descending else order_column)
            
            # Apply limit
            if limit:
                query = query.limit(limit)

            return query.all()

        result = self.execute_transaction(operation)
        return Data(result)
    
    def update(self, model_class, filters, update_fields):
        """Update database records using filters."""
        def operation(session):
            record = session.query(model_class).filter_by(**filters).first()
            if record:
                for key, value in update_fields.items():
                    setattr(record, key, value)
                
            return record

        return self.execute_transaction(operation)

    def bulk_insert(self, model_class, data_list: List[Dict]):
        """Insert multiple records into the database."""
        def operation(session:Session):
            object_list = []
            for data in data_list:
                if data:
                    if isinstance(data, dict):
                        object_list.append(model_class(**data))
                    elif isinstance(data, model_class):
                        object_list.append(data)

            if not object_list:
                print("No data provided for bulk insert")
                return

            session.bulk_save_objects(object_list)
            return len(object_list)

        return self.execute_transaction(operation)

    def bulk_update(self, model_class: type, updates: List[Dict]) -> int:
        """Perform a bulk update of the given model_class with the provided updates.

        Args:
            model_class (type): The SQLAlchemy model class to update.
            updates (List[Dict]): A list of dictionaries, where each dictionary represents
                the column names to update and their respective values.

        Returns:
            int: Number of rows updated.
        """
        if not updates:
            raise ValueError("No updates provided")

        def operation(session):
            row_count = session.bulk_update_mappings(model_class, updates)  # Retrieve number of updated rows
            
            return row_count

        return self.execute_transaction(operation)

    def paginate(self, model_class, conditions: List=None, page: int = 1, per_page: int = 10):
       
        """Retrieve paginated records from the database.
        Args:
            model_class (type): The SQLAlchemy model class to retrieve from.
            conditions (List, optional): A list of SQLAlchemy filter conditions. Defaults to None.
            page (int, optional): The page number to retrieve. Defaults to 1.
            per_page (int, optional): The number of records per page. Defaults to 10.

        Returns:
            List: A list of records retrieved from the database.
        
        ### Example usage of different conditions:
            conditions=[]
            conditions.append(model_class.column_name == 'value')
            conditions.append(model_class.column_name != 'value')
            conditions.append(model_class.column_name.in_(['value', 'value2']))
            conditions.append(model_class.column_name.like('%value%'))
            conditions.append(model_class.column_name.ilike('%value%'))
            conditions.append(model_class.column_name.is_(None))
            conditions.append(model_class.column_name.isnot(None))
            conditions.append(model_class.column_name.between(1, 10))
            conditions.append(model_class.column_name.notbetween(1, 10))
        """
        def operation(session:Session):
            query = session.query(model_class)
            if conditions:
                query = query.filter(and_(*conditions))
                
            offset = (page - 1) * per_page
            records = query.offset(offset).limit(per_page).all()
            
            return records

        return self.execute_transaction(operation)
    
    def delete(self, model_class, conditions: List|str=None,primary_keys:List[Any]=[]) -> int:
        """Delete records from the database based on the given conditions.

        Args:
            model_class (type): The SQLAlchemy model class to delete from.
            conditions (List|str): A list of SQLAlchemy filter conditions or a string 'ALL' to delete all records of the model_class.
            primary_keys (List[Any]): A list of primary key values to delete. If not provided, the primary key of the model_class is determined automatically.

        Returns:
            int: Number of rows deleted.

        ### Example usage of different conditions:
            conditions=[]
            conditions.append(model_class.column_name == 'value')
            conditions.append(model_class.column_name != 'value')
            conditions.append(model_class.column_name.in_(['value', 'value2']))
            conditions.append(model_class.column_name.like('%value%'))
            conditions.append(model_class.column_name.ilike('%value%'))
            conditions.append(model_class.column_name.is_(None))
            conditions.append(model_class.column_name.isnot(None))
            conditions.append(model_class.column_name.between(1, 10))
            conditions.append(model_class.column_name.notbetween(1, 10))

        """
        
       
        conditions = conditions or []
        
        if isinstance(conditions, list) and primary_keys:
            primary_keys_list = list(model_class.__table__.primary_key.columns)
            if not primary_keys_list:
                raise ValueError(f"Model {model_class.__name__} has no primary key!")
            primary_key = primary_keys_list[0].name
            condition = getattr(model_class, primary_key).in_(primary_keys)
            conditions.append(condition)

        
        

        def operation(session:Session):
            if isinstance(conditions, str) and conditions == 'ALL':
                deleted_count = session.query(model_class).delete(synchronize_session=False)
            elif isinstance(conditions, list):
                deleted_count = session.query(model_class).filter(and_(*conditions)).delete(synchronize_session=False)
            else:   
                deleted_count=0
                
            return deleted_count


        result=self.execute_transaction(operation) 
        return result if result is not None else 0

