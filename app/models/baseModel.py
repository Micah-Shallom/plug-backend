from datetime import datetime
from app.extensions import db
from app.utils import generate_uuid
from datetime import timezone

class BaseModel(db.Model):
    
    """
        This class defines all common attributes/methods
        for other class that would inherit it.
    """


    __abstract__ = True

    uid = generate_uuid()

    id = db.Column(db.String(256), primary_key=True, default=uid)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def __init__(self, *args, **kwargs):
        """
            Initialization of base model class

            Args:
                args: Not used
                Kwargs: constructor for the basemodel

            Attributes:
                id: unique id generated
                created_at: creation date
                updated_at: updated date
        """

        # check if parameters were passed while inheriting
        # and assign the to the base class

        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.now(timezone.utc)
                if key != "__class__":
                    setattr(self, key, value)
                if "id" not in kwargs:
                    self.id = self.uid
                if "created_at" not in kwargs:
                    self.created_at = datetime.now(timezone.utc)
                if "updated_at" not in kwargs:
                    self.updated_at = datetime.now(timezone.utc)

        else:
            self.id = self.uid
            self.updated_at = self.created_at = datetime.now(timezone.utc)

        def __str__(self):
            """
                This instance defines the property of the class in a string fmt
                Return:
                    returns a string containing of class name, id and dict
            """
            return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

        def __repr__(self):
            """
                Return:
                    returns a string representation of the calss

            """
            return self.__str__()
        
        def to_dict(self):
            """
                This instance creates a dictionary representation of the classs

                Return:
                    returns a dict rep of the class containing the
            """

            base_dict = dict(self.__dict__)
            base_dict['__class__'] = str(type(self).__name__)
            base_dict['created_at'] = self.created_at.isoformat()
            base_dict['updated_at'] = self.updated_at.isoformat()

            return base_dict
        
        def before_save(self,*args, **kwargs):
            pass

        def after_save(self, *args, **kwargs):
            pass

        def save(self, commit=True):
            """
                This instance saves the current attributes in the class
                and updates the updated_at attribute

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
            pass

        def after_update(self, *args, **kwargs):
            pass

        def update(self, *args, **kwargs):
            self.before_update(*args, **kwargs)
            db.session.commit()
            self.after_update(*args, **kwargs)

        def delete(self, commit=True):
            db.session.delete(self)
            if commit:
                db.session.commit()

        def bulk_create(self, data ,commit=True):
            db.session.add_all(data)
            if commit:
                db.session.commit()