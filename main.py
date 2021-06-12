import pandas as pd
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

    id = Column(Integer, primary_key=True, autoincrement=True)
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
    parser.add_argument("info", help="Load user's info & key")
    parser.add_argument("-d", "--db_name", default='test', help="Choose current database")
    args = parser.parse_args()

    # Create DB
    db_name = args.db_name
    try:
        create_db(db_name)
    except:
        pass

    engine = create_engine(f'{DB_URL}/{db_name}')
    Base.metadata.create_all(engine)

    # Read data
    df = pd.read_csv(args.info)
    print('data:')
    print(df)

    # Initialize session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add records into DB
    for info in df.itertuples():
        user = User(name=info.name, fullname=info.fullname, nickname=info.nickname, key=info.key)
        session.add(user)
        session.commit()

    # Print results
    results = session.query(User).filter_by(nickname='Bomb').all()
    print("\nFind user with nickname=Bomb:")
    for i, result in enumerate(results):
        print(f"{i+1}. {result}")
