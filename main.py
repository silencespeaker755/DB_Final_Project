from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from EncryptedString import EncrypedString
from sqlalchemy.orm import sessionmaker
from CryptoList import RSAKey
from dotenv import load_dotenv
import os
import argparse

load_dotenv()
DB_URL = os.getenv('DB_URL')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(EncrypedString(RSAKey(), 255))
    fullname = Column(EncrypedString(RSAKey(), 255))
    nickname = Column(String(16))
    key = Column((EncrypedString(RSAKey(), 255)))

    def __repr__(self):
        return f"<User(name='{self.name}', fullname='{self.fullname}', nickname='{self.nickname}', key='{self.key}')>"

def create_db(db_name):
    engine = create_engine(DB_URL)
    conn = engine.connect()
    conn.execute(f'create database {db_name} collate utf8mb4_unicode_ci')
    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--db_name", help="Choose current database")
    parser.add_argument("-f", "--info", help="Load user's info & key")
    args = parser.parse_args()

    db_name = args.db_name
    try:
        create_db(db_name)
    except:
        pass

    engine = create_engine(f'{DB_URL}/{db_name}')
    Base.metadata.create_all(engine)

    with open(args.info) as f:
        infos = [[t.strip() for t in line.split(" ")] for line in f.readlines()]

    Session = sessionmaker(bind=engine)
    session = Session()

    for info in infos:
        user = User(name=info[0], fullname=info[1], nickname=info[2], key=info[3])
        session.add(user)
        session.commit()

    our_user = session.query(User).filter_by(nickname='dog').all()
    print(our_user)
