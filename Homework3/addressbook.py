################################################################################
#         Address book classes                                                    #
################################################################################
import re
import json
from collections import UserDict
import math
from datetime import datetime
from abc import ABC, abstractmethod


class AddressBook(UserDict):
    def __init__(self, name, viewer):
        super().__init__()
        self.name = name
        self.current_page = 0
        self.records_on_the_page = 3
        self.viewer = viewer

    def add_record(self, record):
        self.data[record.name.value] = record

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_page < int(math.ceil(len(self.data)/self.records_on_the_page)):
            keys = list(self.data.keys())
            r_list = []  
            for i in range(self.current_page*self.records_on_the_page, min([(self.current_page+1)*self.records_on_the_page, len(self.data)])):
                a_dict = dict()
                a_dict["Name"] = keys[i]
                a_dict["Phones"] = [x.value for x in self.data[keys[i]].phones]
                if self.data[keys[i]].birthday:
                    a_dict["Birthday"] = str(self.data[keys[i]].birthday.value)
                if self.data[keys[i]].address:
                    a_dict["Address"] = self.data[keys[i]].address.value
                if self.data[keys[i]].email:
                    a_dict["Email"] = str(self.data[keys[i]].email.value)
                r_list.append(a_dict)
            self.current_page += 1
            return r_list
        else:
            self.current_page = 0
        raise StopIteration

    def delete(self, name):
        if name in self.data.keys():
            self.data.pop(name)
        else:
            self.viewer("Can't find record")
            
    def dump(self, file):
        with open(file, 'w+') as write_file:
            dump_dict = {self.name: {}}
            store_records_on_the_page = self.records_on_the_page
            self.records_on_the_page = 1
            id = 1
            for page in self:
                dump_dict[self.name]["RecID"+str(id)] = page[0]
                id += 1
            json.dump(dump_dict, write_file)
            self.records_on_the_page = store_records_on_the_page
            
    def load(self, file):
        with open(file, 'r') as read_file:
            data = json.load(read_file)
            
        self.name = list(data.keys())[0]
        for name in list(data[self.name].keys()):
            record = data[self.name][name]
            rec = Record(record["Name"], self.viewer)
            if "Phones" in record.keys():
                for phone in record["Phones"]:
                    rec.add_phone(phone)
            if "Birthday" in record.keys():
                lst = record["Birthday"].split("-")
                rec.add_birthday(lst[2]+"."+lst[1]+"."+lst[0])
            if "Address" in record.keys():
                rec.add_address(record["Address"])
            if "Email" in record.keys():
                rec.add_email(record["Email"])
            self.add_record(rec)

    def find(self, request):
        result_lst = []
        for name in self.data.keys():
            search_list = [name]
            search_list.extend([phone.value for phone in self.data[name].phones])
            for field in search_list:
                if not re.search(request.upper(), field.upper()) is None:
                    result_lst.append(name)
                    break
        return result_lst 


class Record:
    def __init__(self, name, viewer):
        self.phones = list()
        self.birthday = None
        self.email = None
        self.address = None
        self.name = Name(name)
        self.keywords = None
        self.notes = None
        self.viewer = viewer

    def __str__(self):
        str_res = "      Name:       "+str(self.name.value)+"\n"
        if self.phones:
            str_res = str_res+"      Phone list: "
            for p in self.phones:
                str_res = str_res+p.value+"\n                  "

            str_res = str_res[:-18]
        if self.email:
            str_res = str_res + "      Email:      " + self.email.value + "\n"
        if self.address:
            str_res = str_res + "      Address:    \n"
            for key in self.address.value.keys():
                str_res = str_res + " "*18 + key + ":" + " "*(len("apartment")-len(key)) + self.address.value[key] + "\n"
        if self.birthday:
            str_res = str_res+"      Birthday    "+str(self.birthday.value)+"\n"
        str_res = str_res+"-----------------------------------------------------------"
        return str_res

    def add_phone(self, phone):
        if phone not in [ph.value for ph in self.phones]:
            self.phones.append(Phone(phone, self.viewer))

    def add_email(self, email):
        self.email = Email(email, self.viewer)

    def add_address(self, address):
        self.address = Address(address, self.viewer)

    def del_phone(self, phone):
        self.phones = list(filter(lambda x: x.value != phone, self.phones))

    def edit_phone(self, phone, new_phone):
        if phone in [x.value for x in self.phones]:
            self.del_phone(phone)
            self.add_phone(new_phone)
       
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday, self.viewer)

    def days_to_birthday(self):
        current_date = datetime.now().date()
        if self.birthday:
            birthday_date = self.birthday.value.replace(year=current_date.year)
            delta = birthday_date - current_date
            if delta.days < 0:
                new_birthday_date = birthday_date.replace(year=birthday_date.year + 1)
                delta = new_birthday_date - current_date
                return delta.days
            else:
                delta = birthday_date - current_date
                return delta.days
        return 1000


class Field:
    def __init__(self, value, viewer):
        self.value = value
        self.viewer = viewer

    def __str__(self):
        self.viewer(f"{self.__dict__}")

    @property
    def value(self):
       return self.__value    

    @value.setter
    def value(self, value_):
       if len(value_) > 0:
          self.__value = value_


class Name(Field):
    def __init__(self, name):
        self.__value = name

    @property
    def value(self):
       return self.__value    

    @value.setter
    def set_value(self, name):
       if len(self.value) > 0:
          self.__value = name    


class Phone(Field):
    def __init__(self, phone, viewer):
        self.value = phone
        self.viewer = viewer

    @property
    def value(self):
       return self.__value

    @value.setter
    def value(self, phone):
       if not re.search(r'\+\d{12}', phone) is None:
          self.__value = phone
       else:
          self.viewer("Phone should have format: '[+] [XX] XXXXXXXXXX' (9 or 12 digits)")
          raise ValueError("Incorrect phone format")


class Email(Field):
    def __init__(self, email, viewer):
        self.__value = None
        self.value = email
        self.viewer = viewer

    @property
    def value(self):
       return self.__value

    @value.setter
    def value(self, email):
       if not re.search(r'[a-zA-Z0-9\.\-\_]+@[a-zA-Z0-9\-\_\.]+\.[a-z]{2,4}', email) is None:
          self.__value = email
       else:
          self.viewer("Email should have format: 'name@domain.[domains.]high_level_domain'")
          raise ValueError("Incorrect email format")


class Address(Field):
    def __init__(self, address, viewer):
        self.__value = None
        self.value = address
        self.viewer = viewer

    @property
    def value(self):
       return self.__value

    @value.setter
    def value(self, address):
       self.__value = address

       
class Birthday(Field):
    def __init__(self, birthday, viewer):
        self.__value = None
        self.value = birthday
        self.viewer = viewer

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, birthday):
        if re.search(r'\d{2}.\d{2}.\d{4}', birthday):
            self.__value = datetime.strptime(birthday, '%d.%m.%Y').date()
        else:
            return False


class Interface(ABC):
    @abstractmethod
    def view(self, *args):
        pass


class ViewerInterface(Interface):
    def view(self, *args):
        print(*args)
