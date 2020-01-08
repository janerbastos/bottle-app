import bcrypt
from sqlalchemy import Column, Integer, String, Sequence, Boolean, DateTime
from datetime import datetime
from core import Base



class User(Base):
    
    __tablename__ = 'auth'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    username = Column(String(150), unique=True, nullable=False)
    hashed = Column(String(128), nullable=False)
    salt = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False, unique=True)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    date_joined = Column(DateTime, default=datetime.utcnow())
    last_login = Column(DateTime)


    def gerar_hashed(self, password):
        salt = bcrypt.gensalt(8)
        self.salt = str(salt, 'utf-8')
        self.hashed = bcrypt.hashpw(str.encode(password), salt)

    def __init__(self, first_name, last_name, username, email, password=None, active=True):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.is_active = active
        if password:
            self.gerar_hashed(password)
            
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': '%s %s' % (self.first_name, self.last_name),
            'email': self.email,
            'is_superuser': self.is_superuser,
            'is_staff': self.is_staff,
            'date_joined': str(self.date_joined),
            'last_login': str(self.last_login) if self.last_login else ''
        }

    def __repr__(self):
        return "<User(username='%s', email='%s')>" % (self.username, self.email)