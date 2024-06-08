from datetime import datetime
from app.extensions import db
from app.utils import generate_uuid as uuid
from datetime import timezone
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel(db.Model):
    """
    Base model class defining common attributes and methods for other classes.
    """

    __abstract__ = True

    # Primary key using UUID as a string
    id = db.Column(db.String(256), primary_key=True, default=str(uuid()))

    # Creation timestamp in UTC timezone
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Last update timestamp in UTC timezone, nullable for initial creation
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def __init__(self, *args, **kwargs):
        """
        Initialization of the base model class.

        Args:
            *args: Not used.
            **kwargs: Constructor for the base model.

        Attributes:
            id: Unique ID generated.
            created_at: Creation datetime.
            updated_at: Updated datetime.
        """

        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.now(timezone.utc)
                if key != "__class__":
                    setattr(self, key, value)

            # Initialize id, created_at, updated_at if not provided
            if "id" not in kwargs:
                self.id = str(uuid())
            if "created_at" not in kwargs:
                self.created_at = datetime.now(timezone.utc)
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now(timezone.utc)

        else:
            # Initialize with default values
            self.id = str(uuid())
            self.updated_at = self.created_at = datetime.now(timezone.utc)

    def __str__(self):
        """
        String representation of the instance.

        Return:
            String containing class name, id, and instance dictionary.
        """
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def __repr__(self):
        """
        String representation of the instance.

        Return:
            String representation.
        """
        return self.__str__()

    def to_dict(self):
        """
        Dictionary representation of the instance.

        Return:
            Dictionary representation containing class name and attributes.
        """
        base_dict = dict(self.__dict__)
        base_dict['__class__'] = str(type(self).__name__)
        base_dict['created_at'] = self.created_at.isoformat()
        base_dict['updated_at'] = self.updated_at.isoformat()

        return base_dict

    def before_save(self):
        """Hook method called before saving."""
        pass

    def after_save(self):
        """Hook method called after saving."""
        pass

    def save(self, commit=True):
        """
        Save the current instance to the database.

        Args:
            commit (bool): Whether to commit the transaction immediately.

        Return:
            None
        """
        self.before_save()
        db.session.add(self)
        if commit:
            try:
                self.updated_at = datetime.now(timezone.utc)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
        self.after_save()

    def before_update(self, *args, **kwargs):
        """Hook method called before updating."""
        pass

    def after_update(self, *args, **kwargs):
        """Hook method called after updating."""
        pass

    def update(self, *args, **kwargs):
        """
        Update the current instance in the database.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Return:
            None
        """
        self.before_update(*args, **kwargs)
        db.session.commit()
        self.after_update(*args, **kwargs)

    def delete(self, commit=True):
        """
        Delete the current instance from the database.

        Args:
            commit (bool): Whether to commit the transaction immediately.

        Return:
            None
        """
        db.session.delete(self)
        if commit:
            db.session.commit()

    def bulk_create(self, data, commit=True):
        """
        Bulk create instances in the database.

        Args:
            data (list): List of instances to create.
            commit (bool): Whether to commit the transaction immediately.

        Return:
            None
        """
        db.session.add_all(data)
        if commit:
            db.session.commit()
