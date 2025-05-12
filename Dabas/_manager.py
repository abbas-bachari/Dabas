from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy import Engine, or_, and_
from typing import List, Dict
from ._data import Data



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
    
    
    def insert(self, model_instance):
        """Add a new record to the database."""
        def operation(session:Session):
            
            session.add(model_instance)
            
            return True

        return self.execute_transaction(operation)
    
    def get(self, model_class, limit=None, filters={}, order_by=None, descending=False):
        """Retrieve sorted data based on filters and order criteria.

        Args:
            model_class (type): The SQLAlchemy model class to retrieve.
            limit (int): Maximum number of records to return.
            filters (dict): Filtering conditions.
            order_by (str): Column name for ordering results.
            descending (bool): If True, sorts in descending order.

        Returns:
            Data: Retrieved database records.
        """

        def operation(session):
            query = session.query(model_class)
            
            # Apply filters
            for key, value in filters.items():
                query = query.filter(getattr(model_class, key) == value)

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
    
    def get_all(
            self, 
            model_class, 
            limit=None, 
            order_by=None,
            descending=False, 
            filters={}, 
            range_filters={},
            or_conditions=[],
            and_conditions=[]
            ):
        
        """Retrieve sorted data based on filters and order criteria.

        Args:
            model_class (type): The SQLAlchemy model class to retrieve.
            limit (int): Maximum number of records to return.
            filters (dict): Filtering conditions.
            order_by (str): Column name for ordering results.
            descending (bool): If True, sorts in descending order.
        
        ## Example usage:
        ### Search for all data with column="Field" and price between 100000 and 200000
        results = get_all(model_class, filters={"column": "Field"}, range_filters={"price": (100000, 200000)})
        print(results.to_dict())

        ### Search with OR conditions: data with column="Field_1" or column="Field_2"
        results = get_all(model_class, or_conditions=[("column", "Field_1"), ("column", "Field_2")])
        print(results.to_dict())

        ### Search with AND conditions: data with column="Field_1" and column="Field_2"
        results = get_all(model_class, and_conditions=[("column", "Field_1"), ("column", "Field_2")])
        print(results.to_dict())


        ### Limit the number of results to 5 data
        results = get_all(model_class, filters={"column": "Field"}, limit=5)
        print(results.to_dict())

        Returns:
            Data: Retrieved database records.
        """

        def operation(session):
            query = session.query(model_class)
            
            # Apply filters
            for key, value in filters.items():
                query = query.filter(getattr(model_class, key) == value)

            
            # Apply range filters (e.g., between two values)
            for key, (low, high) in range_filters.items():
                query = query.filter(getattr(model_class, key).between(low, high))

            # Apply OR conditions
            if or_conditions:
                or_filters = [getattr(model_class, key) == value for key, value in or_conditions]
                query = query.filter(or_(*or_filters))
            
            # Apply AND conditions
            if and_conditions:
                and_filters = [getattr(model_class, key) == value for key, value in and_conditions]
                query = query.filter(and_(*and_filters))
            
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
    
    def search(self, model_class, filters={}, range_filters={}, or_conditions=[],and_conditions=[], limit=None):
        """Advanced search based on exact filters, range filters, and OR conditions.

        ## Example usage:
        ### Search for all data with column="Field" and price between 100000 and 200000
        results = search(model_class, filters={"column": "Field"}, range_filters={"price": (100000, 200000)})
        print(results.to_dict())

        ### Search with OR conditions: data with column="Field_1" or column="Field_2"
        results = search(model_class, or_conditions=[("column", "Field_1"), ("column", "Field_2")])
        print(results.to_dict())

        ### Search with AND conditions: data with column="Field_1" and column="Field_2"
        results = search(model_class, and_conditions=[("column", "Field_1"), ("column", "Field_2")])
        print(results.to_dict())


        ### Limit the number of results to 5 data
        results = search(model_class, filters={"column": "Field"}, limit=5)
        print(results.to_dict())
        """
        def operation(session):
            query = session.query(model_class)

            # Apply exact filters
            for key, value in filters.items():
                query = query.filter(getattr(model_class, key) == value)

            # Apply range filters (e.g., between two values)
            for key, (low, high) in range_filters.items():
                query = query.filter(getattr(model_class, key).between(low, high))

            # Apply OR conditions
            if or_conditions:
                or_filters = [getattr(model_class, key) == value for key, value in or_conditions]
                query = query.filter(or_(*or_filters))
            # Apply AND conditions
            if and_conditions:
                and_filters = [getattr(model_class, key) == value for key, value in and_conditions]
                query = query.filter(and_(*and_filters))
            
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
        def operation(session):
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

    def paginate(self, model_class, filters={}, page: int = 1, per_page: int = 10):
        """Retrieve paginated results from the database.

        Args:
            model_class (type): The SQLAlchemy model class to retrieve.
            filters (Dict): Filtering conditions.
            page (int): The current page number.
            per_page (int): Number of records per page.

        Returns:
            List: Paginated records.
        """
        def operation(session):
            query = session.query(model_class)
            for key, value in filters.items():
                query = query.filter(getattr(model_class, key) == value)
            offset = (page - 1) * per_page
            records = query.offset(offset).limit(per_page).all()
            
            return records

        return self.execute_transaction(operation)
    
    def delete(self, model_class, filters: Dict) -> int:
            """Delete records from the database based on filters.

            Args:
                model_class (type): The SQLAlchemy model class to delete from.
                filters (Dict): The filtering conditions.

            Returns:
                int: Number of records deleted.
            """
            def operation(session):
                records = session.query(model_class).filter_by(**filters).all()
                if records:
                    deleted_count = len(records)
                    for record in records:
                        session.delete(record)
                    
                    return deleted_count
                print("No matching records found for deletion.")
                return 0

            return self.execute_transaction(operation)
    