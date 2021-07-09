################################################################################
#         Address book classes                                                    #
################################################################################
import re
import json
from collections import UserDict
import math
from datetime import datetime


class AddressBook(UserDict):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.current_page = 0
        self.records_on_the_page = 3
        self.viewer = ViewerInterface().view

    def add_record(self,record):
        self.data [record.name.value] = record

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_page < int(math.ceil(len(self.data)/self.records_on_the_page)):
            keys = list(self.data.keys())
            r_list = []  
            for i in range(self.current_page*self.records_on_the_page, min([(self.current_page+1)*self.records_on_the_page, len(self.data)])):
                a_dict = {}    
                a_dict["Name"] = keys[i]
                a_dict["Phones"] = [x.value for x in self.data[keys[i]].phones]
                if type(self.data[keys[i]].birthday) != type(""):
                    a_dict["Birthday"] = str(self.data[keys[i]].birthday.value)
                if type(self.data[keys[i]].address) != type(""):
                    a_dict["Address"] = self.data[keys[i]].address.value
                if type(self.data[keys[i]].email) != type(""):
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
            print("Can't find record")
            
    def dump(self, file):
        with open(file, 'w+') as write_file:
            dump_dict = {self.name:{}}
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
                rec = Record(record["Name"])
                if "Phones" in record.keys():
                    for phone in record["Phones"]:
                        rec.add_phone(Phone(phone))
                if "Birthday" in record.keys():
                    lst = record["Birthday"].split("-")
                    birthday = Birthday(lst[2]+"."+lst[1]+"."+lst[0])
                    rec.add_birthday(birthday)
                if "Address" in record.keys():
                    rec.add_address(Address(record["Address"]))
                if "Email" in record.keys():
                    rec.add_email(Email(record["Email"]))
                self.add_record(rec)

    def find(self, request):
        result_lst = []
        for name in self.data.keys():
            search_list = [name]
            search_list.extend([phone.value for phone in self.data[name].phones])
            for field in search_list:
                if re.search(request.upper(), field.upper()) != None:
                    result_lst.append(name)
                    break
        return result_lst 


class Record:
    def __init__(self, name):
        self.phones = list()
        self.birthday = ""
        self.email = ""
        self.address=""
        self.name = Name(name)

    def __str__(self):
        str_res = "      Name:       "+str(self.name.value)+"\n"
        if self.phones != []:
            str_res = str_res+"      Phone list: "
            for p in self.phones:
                str_res = str_res+p.value+"\n                  "

            str_res = str_res[:-18]
        if type(self.email) != type(""):
            str_res = str_res+"      Email:      "+self.email.value+"\n"
        if type(self.address) != type(""):
            str_res = str_res+"      Address:    \n"
            for key in self.address.value.keys():
                str_res = str_res+"                  "+key+":"+" "*(len("apartment")-len(key))+self.address.value[key]+"\n"
        if type(self.birthday) != type(""):
             str_res = str_res+"      Birthday    "+str(self.birthday.value)+"\n"
        str_res = str_res+"-----------------------------------------------------------"
        return str_res

    def add_keywords(self, keywords):
        self.keywords = keywords

    def add_notes(self, notes):
        self.notes = notes
      
    def add_phone(self, phone):
        if phone.value not in [ph.value for ph in self.phones]:
            self.phones.append(phone)

    def add_email(self, email):
        self.email = email

    def add_address(self, address):
        self.address = address         

    def del_phone(self, phone):
        self.phones = list(filter(lambda x: x.value != phone, self.phones))

    def edit_phone(self, phone, new_phone):
        if phone in [x.value for x in self.phones]:
            self.del_phone(phone)
            self.add_phone(Phone(new_phone))
       
    def add_birthday(self,birthday):
        self.birthday = birthday

    def days_to_birthday(self):
        if type(self.birthday) != type(""):
            date1 = datetime(datetime.now().timetuple().tm_yday, self.birthday.value.timetuple().tm_mon, self.birthday.value.timetuple().tm_mday)
            delta = date1.timetuple().tm_yday - datetime.now().timetuple().tm_yday
            if delta > 0:
                return str(delta)
            else:
                date1 = datetime(datetime.now().timetuple().tm_year+1, self.birthday.value.timetuple().tm_mon, self.birthday.value.timetuple().tm_mday)
                date2 = datetime(datetime.now().timetuple().tm_year, datetime.now().timetuple().tm_mon, datetime.now().timetuple().tm_mday)
                delta = date1 - date2
            return str(delta.days)
        return str(1000)


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        print(f"{self.__dict__}")

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
    def __init__(self, phone):
        self.value = phone

    @property
    def value(self):
       return self.__value

    @value.setter
    def value(self, phone):
       if re.search('\+\d{12}', phone) != None:
          self.__value = phone
       else:
          print("Phone should have format: '[+] [XX] XXXXXXXXXX' (9 or 12 digits)")  
          raise  ValueError("Incorrect phone format")


class Email(Field):
    def __init__(self, email):
        self.value = email

    @property
    def value(self):
       return self.__value

    @value.setter
    def value(self, email):
       if re.search('[a-zA-Z0-9\.\-\_]+@[a-zA-Z0-9\-\_\.]+\.[a-z]{2,4}', email) != None:
          self.__value = email
       else:
          print("Email should have format: 'name@domain.[domains.]high_level_domain'")  
          raise  ValueError("Incorrect email format")


class Address(Field):
    def __init__(self, address):
        self.value = address

    @property
    def value(self):
       return self.__value

    @value.setter
    def value(self, address):
       self.__value = address

        
       
class Birthday(Field):
    def __init__(self, birthday):
        self.value = birthday

    @property
    def value(self):
       return self.__value

    @value.setter
    def value(self, birthday):
       if re.search('\d{2}\.\d{2}\.\d{4}', birthday) != None:
          self.__value = datetime.strptime(birthday, '%d.%m.%Y').date()
       else:
          return False


class ViewerInterface:
    def view(self, data):
        print(data)