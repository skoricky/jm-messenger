import os
import json
from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Client(Base):
    __tablename__ = 'client'
    client_id = Column(Integer, primary_key=True)
    name = Column(String)
    info = Column(String)

    def __init__(self, name, info=None):
        self.name = name
        self.info = info


class HistoryClient(Base):
    __tablename__ = 'history_client'
    id = Column(Integer, primary_key=True)
    client_ip = Column(String)
    time = Column(String)
    date = Column(String)

    def __init__(self, client_ip, time, date):
        self.client_ip = client_ip
        self.time = time
        self.date = date


class ContactList(Base):
    __tablename__ = 'contact_list'
    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer)
    client_id = Column(Integer)
    info = Column(String)

    def __init__(self, client_id, contact_id, info=None):
        self.client_id = client_id
        self.contact_id = contact_id
        self.info = info


def create_repository():
    return SqliteDbRepository(metadata)


class JRepository:
    """
    Базовый класс Хранилище (с примером сохранения в json)
    """
    pass


class JsonFileRepository(JRepository):
    DIR_NAME = 'json'
    FILE_NAME = 'test.json'
    CUR_DIR_PATH = os.path.dirname(__file__)
    FILE_PATH = os.path.join(os.path.abspath(CUR_DIR_PATH), DIR_NAME, FILE_NAME)

    def __init__(self, data):
        self.data = data
        self.set_datainfile()

    def set_datainfile(self):
        print(self.FILE_PATH)
        with open(self.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(self.data, file)


class PostgresDbRepository(JRepository):
    pass


class SqliteDbRepository(JRepository):
    def __init__(self, metadata):
        self.engine = create_engine('sqlite:///repository//sqltdb//sqltdb.sqlite')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        metadata.create_all(self.engine)

    def add_client(self, name):
        if not self.session.query(Client).filter_by(name=name).first():
            self.session.add(Client(name))
            self.session.commit()

    def add_session(self, client_ip):
        self.session.add(HistoryClient(client_ip, str(datetime.now().time()), str(datetime.now().date())))
        self.session.commit()

    def get_contactlist(self, client_id):
        contactlist = []
        query = self.session.query(ContactList).filter_by(client_id=client_id).order_by(ContactList.contact_id).all()
        for _ in query:
            contactlist.append(self.session.query(Client).filter_by(client_id=_.contact_id).first().name)
        return contactlist

    def add_contact(self, client_name, contact_name):
        client_id = self.session.query(Client).filter_by(name=client_name).first().client_id
        contact_id = self.session.query(Client).filter_by(name=contact_name).first().client_id
        query = self.session.query(ContactList).filter_by(client_id=client_id, contact_id=contact_id).first()
        if not query and client_id and contact_id:
            self.session.add(ContactList(client_id, contact_id))
            self.session.commit()

    def del_contact(self, client_name, contact_name):
        client_id = self.session.query(Client).filter_by(name=client_name).first().client_id
        contact_id = self.session.query(Client).filter_by(name=contact_name).first().client_id
        query = self.session.query(ContactList).filter_by(client_id=client_id, contact_id=contact_id).first()
        if query:
            self.session.delete(query)
            self.session.commit()



if __name__ == '__main__':
    data = {"name": "admin"}
    JsonFileRepository(data)

    # l = SqliteDbRepository(metadata)
    l = create_repository()

    # new_cli = Client("vasia", "new")
    # new_cli1 = Client("stefan", "new")
    #
    # new_con = ContactList(1, 2)
    # l.session.add_all(new_con)
    # l.session.commit()
    #
    # l.session.add_all([new_cli, new_cli1, new_con])
    # l.session.commit()

    l.add_client("sasha")

    _list = l.get_contactlist(1)

    for i in _list:
        print(i)

    # l.del_contact("vasia", "stefan")
    l.add_contact("sasha", "vasia")
    l.add_session("192.168.0.3")
