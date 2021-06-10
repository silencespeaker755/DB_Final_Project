from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from EncryptedString import EncrypedString
from sqlalchemy.orm import sessionmaker
from CryptoList import CaesarCipher
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv('DB_URL')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(16))
    fullname = Column(String(16))
    nickname = Column(EncrypedString(CaesarCipher(3), 255))

    def __repr__(self):
        return f"<User(name='{self.name}', fullname='{self.fullname}', nickname='{self.nickname}')>"

def create_db(db_name):
    engine = create_engine(DB_URL)
    conn = engine.connect()
    conn.execute(f'create database {db_name} collate utf8mb4_unicode_ci')
    conn.close()

if __name__ == '__main__':
    db_name = 'test_db'
    try:
        create_db(db_name)
    except:
        pass

    engine = create_engine(f'{DB_URL}/{db_name}')
    Base.metadata.create_all(engine)

    ed_user = User(name='ed', fullname='Ed Jones', nickname='eds')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.add(ed_user)
    session.commit()

    our_user = session.query(User).filter_by(name='ed').all()
    print(our_user)
