from sqlalchemy import create_engine, Column, String, CHAR
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import mysql.connector
import hashlib

ssl_ca = "/etc/ssl/cert.pem"
engine = create_engine('mysql+pymysql://acheljyoppwu0y25616n:pscale_pw_nksjglGGyQgDI8jyIyzgrfTpwwgQ6uJk6Uww2SuDPgo@aws.connect.psdb.cloud/galactic_gains?charset=utf8mb4', connect_args={'ssl': {'ca': ssl_ca}})

Base = declarative_base()
Base.metadata.bind = engine


from sqlalchemy import Column, String
class User(Base):
    __tablename__ = 'users'

    email = Column(String(255), primary_key=True)
    password = Column(String(255))
    accountType = Column(String(1))

Session = sessionmaker(bind=engine)
session = Session()



def verifyLogin(email, password):
    user = session.query(User).filter_by(email=email).first()
    print(user)
    if user:
        if user.password == hashlib.sha256(password.encode()).hexdigest():
            return True
        return False
    return False


def verifyAccountCreation(email, password, confirmPassword):
    if confirmPassword != password:
        return "Passwords dont match!"
    user = session.query(User).filter_by(email=email).first()

    if user:
        return "Account already exists"

    new_user = User(email=email, password=hashlib.sha256(password.encode()).hexdigest(), accountType='A')
    session.add(new_user)
    session.commit()
    return None




