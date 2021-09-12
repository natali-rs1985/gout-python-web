from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column, Integer, String, Unicode, Date, Table

import re
from datetime import datetime

from load import Base, metadata, session


phone_record_table = Table(
    'phone_record',
    metadata,
    Column('record_id', ForeignKey('record.record_id', ondelete='CASCADE'), primary_key=True),
    Column('phone_id', ForeignKey('phone.phone_id', ondelete='CASCADE'), primary_key=True)
)


class Record(Base):
    __tablename__ = 'record'
    record_id = Column('record_id', Integer, primary_key=True)
    name_id = Column(Integer, ForeignKey('username.name_id'), unique=True, nullable=False)
    email_id = Column(Integer, ForeignKey('email.email_id', ondelete='CASCADE'))
    address_id = Column(Integer, ForeignKey('address.address_id', ondelete='CASCADE'))
    birthday_id = Column(Integer, ForeignKey('birthday.birthday_id', ondelete='CASCADE'))
    phones = relationship('Phone', secondary=phone_record_table, back_populates='record', cascade='all, delete')
    username = relationship('Name', back_populates='record', cascade='all, delete')
    email = relationship('Email', back_populates='record', cascade='all, delete')
    address = relationship('Address', back_populates='record', cascade='all, delete')
    birthday = relationship('Birthday', back_populates='record', cascade='all, delete')

    def __repr__(self):
        return f'name={self.username}  \nphones={self.phones}  \nemail={self.email}' \
               f'  \naddress: \n{self.address}  \nbirthday: {self.birthday}'

    def __init__(self, username):
        self.username = username
        self.current_page = 0
        self.records_on_the_page = 3

    def __str__(self):
        str_res = "      Name:          " + str(self.username) + "\n"
        if self.phones:
            str_res = str_res + "      Phone list:    "
            for p in self.phones:
                str_res = str_res + str(p) + "\n                  "

            str_res = str_res[:-18]
        if self.email:
            str_res = str_res + "      Email:         " + str(self.email) + "\n"
        if self.address:
            str_res = str_res + "      Address:       " + str(self.address) + "\n"
        if self.birthday:
            str_res = str_res + "      Birthday:      " + str(self.birthday) + "\n"
        str_res = str_res + "-----------------------------------------------------------"
        return str_res

    def add_phone(self, phone):
        if phone not in [ph.phone for ph in self.phones]:
            self.phones.append(Phone(phone=phone))
            session.commit()

    def add_email(self, email):
        self.email = Email(email=email)
        session.commit()

    def add_address(self, address):
        self.address = Address(address=address)
        session.commit()

    def del_phone(self, phone):
        phone = session.query(Phone).filter_by(phone=phone).first()
        session.delete(phone)
        session.commit()

    def edit_phone(self, phone, new_phone):
        if phone in [x.phone for x in self.phones]:
            self.del_phone(phone)
            self.add_phone(new_phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday=birthday)
        session.commit()

    def days_to_birthday(self):
        current_date = datetime.now().date()
        if self.birthday:
            birthday_date = self.birthday.birthday.replace(year=current_date.year)
            delta = birthday_date - current_date
            if delta.days < 0:
                new_birthday_date = birthday_date.replace(year=birthday_date.year + 1)
                delta = new_birthday_date - current_date
                return delta.days
            else:
                delta = birthday_date - current_date
                return delta.days
        return 1000

    def delete(self, name):
        record = session.query(Record).join(Record.username).filter(Name.username == name).first()
        if name in self.data.keys():
            session.delete(record)
            session.commit()
            self.data.pop(name)
        else:
            print("Can't find record")

    def find(self, request):
        result_lst = []
        for name in self.username.username:
            search_list = [name]
            search_list.extend([phone.phone for phone in self.phones])
            for field in search_list:
                if not re.search(request.upper(), field.upper()) is None:
                    result_lst.append(name)
                    break
        return result_lst


class Name(Base):
    __tablename__ = 'username'
    name_id = Column('name_id', Integer, primary_key=True)
    username = Column('username', Unicode(50), nullable=False)
    record = relationship('Record', back_populates='username')

    def __repr__(self):
        return self.username

    def __init__(self, username):
        self.username = username


class Phone(Base):
    __tablename__ = 'phone'
    phone_id = Column('phone_id', Integer, primary_key=True)
    phone = Column('phone', String(13), nullable=False)
    record = relationship('Record', secondary=phone_record_table, back_populates='phones')

    def __init__(self, phone=phone):
        self.phone = phone

    def __repr__(self):
        return self.phone


class Email(Base):
    __tablename__ = 'email'
    email_id = Column('email_id', Integer, primary_key=True)
    email = Column('email', String(50), nullable=False)
    record = relationship('Record', back_populates='email')

    def __repr__(self):
        return self.email

    def __init__(self, email=email):
        self.email = email


class Address(Base):
    __tablename__ = 'address'
    address_id = Column('address_id', Integer, primary_key=True)
    address = Column('country', Unicode(250))
    record = relationship('Record', back_populates='address')

    def __repr__(self):
        return self.address

    def __init__(self, address):
        self.address = address


class Birthday(Base):
    __tablename__ = 'birthday'
    birthday_id = Column('birthday_id', Integer, primary_key=True)
    birthday = Column('birthday', Date, nullable=False)
    record = relationship('Record', back_populates='birthday')

    def __repr__(self):
        return str(self.birthday)

    def __init__(self, birthday=birthday):
        self.birthday = birthday


# metadata.create_all(engine)
