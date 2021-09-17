from fuzzywuzzy import process
import warnings
from mongo_db import contacts_collection as contacts
from load import viewer
import re
from datetime import datetime
from redis_db import redis


warnings.filterwarnings('ignore')
exit_command = ["good bye", "close", "exit"]


def format_phone_number(func):
    def inner(phone):
        result = func(phone)
        if len(result) == 12:
            result = '+' + result
        elif len(result) == 10:
            result = '+38' + result
        return result

    return inner


@format_phone_number
def sanitize_phone_number(phone):
    new_phone = (
        phone.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
    )
    return new_phone


def hello_(data):
    return "How can I help You?"


redis_list = []


def conv_rec(rec):
    name = rec['name']
    phones = ''
    email = ''
    address = ''
    birthday = ''
    if 'phones' in rec:
        phones = ' '.join(rec['phones'])
    if 'email' in rec:
        email = rec['email']
    if 'address' in rec:
        address = rec['address']
    if 'birthday' in rec:
        birthday = str(rec['birthday'].date())
    return name, phones, email, address, birthday


def insert_in_redis(name):
    rec = find_name(name)
    name, phones, email, address, birthday = conv_rec(rec)
    redis.hmset(name, {'name': name})
    if phones:
        redis.hmset(name, {'phones': phones})
    if email:
        redis.hmset(name, {'email': email})
    if address:
        redis.hmset(name, {'address': address})
    if birthday:
        redis.hmset(name, {'birthday': birthday})
    return 1


def verify_redis_list(name):
    if name not in redis_list and len(redis_list) < 3:
        insert_in_redis(name)
        redis_list.insert(0, name)
    elif name in redis_list:
        redis_list.remove(name)
        redis_list.insert(0, name)
    else:
        insert_in_redis(name)
        redis_list.insert(0, name)
        redis_list.pop()
    return redis_list


def find_contact(data):
    viewer("Please input the name")
    name = input().rstrip()
    if name in redis_list:
        rez = find_in_redis(name)
        viewer("Found contact:")
        viewer(print_one(rez))
        redis_list.remove(name)
        redis_list.insert(0, name)
    else:
        res = find_name(name)
        if not res:
            viewer("Can't find record in the phone book")
        else:
            verify_redis_list(name)
            viewer("Found contact:")
            viewer(print_one(res))
    return "How can I help you?"


def find_in_redis(name):
    rez = {}
    val = redis.hmget(name, 'name', 'phones', 'email', 'address', 'birthday')
    rez['name'] = val[0].decode('utf-8')
    if val[1]:
        rez['phones'] = val[1].decode('utf-8').split(' ')
    if val[2]:
        rez['email'] = val[2].decode('utf-8')
    if val[3]:
        rez['address'] = val[3].decode('utf-8')
    if val[4]:
        birthday = datetime.strptime(val[4].decode('utf-8'), '%Y-%m-%d')
        rez['birthday'] = birthday
    return rez


def add_phone(r):
    while True:
        phone = choose_phone()
        if phone == 'exit':
            return 0
        if 'phones' in r:
            if phone not in [ph for ph in r['phones']]:
                try:
                    r['phones'].append(phone)
                    viewer("Phone number successfully added")
                    return r
                except:
                    viewer("Incorrect phone format. Try again or type 'Exit'")
                    continue
            else:
                viewer("This number already belonged to contact " + r['name'] + ", please try again")
        else:
            r['phones'] = []
            try:
                r['phones'].append(phone)
                viewer("Phone number successfully added")
                return r
            except:
                viewer("Incorrect phone format. Try again or type 'Exit'")
                continue


def add_email(r):
    while True:
        viewer("Input email for the contact " + r['name'])
        email = input()
        is_correct_format = re.search(r'[a-zA-Z0-9\.\-\_]+@[a-zA-Z0-9\-\_\.]+\.[a-z]{2,4}', email)
        if email == 'exit':
            return 0
        elif is_correct_format:
            r['email'] = email
            viewer("Email successfully added")
            return r
        else:
            viewer("Email should have format: 'name@domain.[domains.]high_level_domain'. "
                   "Incorrect email format. Try again or type 'Exit'")


def add_address(r):
    viewer("Input address for the contact " + r['name'])
    address = input()
    r['address'] = address
    viewer("Address successfully added")
    return r


def add_birthday(r):
    while True:
        viewer("Please enter the date of birthday in format dd.mm.yyyy")
        birthday = input().lower()
        is_correct_format = re.search(r'\d{2}.\d{2}.\d{4}', birthday)
        if birthday == 'exit':
            viewer("Operation cancelled")
            break
        elif is_correct_format:
            try:
                birthday = datetime.strptime(birthday, '%d.%m.%Y')
                r['birthday'] = birthday
                viewer("Birthday set successfully")
                return r
            except:
                viewer('Date has incorrect format, please try again')
                continue
        viewer("Date has incorrect format, please try again or type 'Exit' to come back to main menu")


def find_name(name):
    name = contacts.find_one({'name': name})
    return name


def find_all():
    users = list(contacts.find())
    return users


def add_contact(data):
    rec = {}
    while True:
        viewer("Input the name of a contact")
        name = input()
        find = find_name(name)
        if not find:
            rec['name'] = name
            break
        else:
            viewer("Contact already exists. Try again")

    while True:
        viewer("Type 'P' to add phone, 'O' skip to other details")
        choose = input().lower()
        if choose == 'p':
            rec = add_phone(rec)
        if choose == 'o':
            viewer("OK, let's go ahead")
            break

    while True:
        viewer("Type 'E to enter e-mail, 'O' skip to other details")
        choose = input().lower()
        if choose == 'e':
            add_email(rec)
            break
        if choose == 'o':
            viewer("OK, let's go ahead")
            break

    while True:
        viewer("Type 'A to enter address, 'O' skip to other details")
        choose = input().lower()
        if choose == 'a':
            add_address(rec)
            break
        if choose == 'o':
            viewer("OK, let's go ahead")
            break

    while True:
        viewer("Type 'B' to enter birthday,'F' to finish")
        choose = input().lower()
        if choose == 'b':
            add_birthday(rec)
            break
        if choose == 'f':
            break
    contacts.insert_one(rec)
    viewer("New contact details:")
    viewer(print_one(rec))
    return "How can I help you?"


def edit_contact(command):
    viewer("Please enter the name of a contact")
    name = edit_name()

    while True:
        viewer("Type 'P' to edit phones, 'O' skip to other details")
        choose = input().lower()
        rec = find_name(name)
        if choose == 'p':
            viewer("Existing phone numbers for the " + rec['name'])
            if 'phones' in rec:
                for ph in rec['phones']:
                    viewer("      " + str(ph))
            while True:
                viewer("Type 'A' to add  phone, 'E' to edit, 'D' for delete, 'O' skip to other details")
                choose_p = input().lower()
                if choose_p == 'a':
                    edit_phones(rec)
                elif choose_p == 'e':
                    while True:
                        rec = find_name(name)
                        viewer("I need the old number to change")
                        phone = input()
                        if phone == 'exit':
                            viewer("Operation cancelled")
                            break
                        if 'phones' in rec:
                            if phone in [ph for ph in rec['phones']]:
                                viewer("I need the new number to save")
                                phone_new = choose_phone()
                                contacts.update_one({'name': name}, {'$pull': {'phones': phone}})
                                contacts.update_one({'name': name}, {'$push': {'phones': phone_new}})
                                viewer("Phone changed successfully")
                                break
                            else:
                                viewer("This number doesn't belong to " + name)
                                continue

                elif choose_p == 'd':
                    while True:
                        rec = find_name(name)
                        viewer("Input the number you would like to delete")
                        phone = input()
                        if phone == 'exit':
                            viewer("Operation cancelled")
                            break
                        if 'phones' in rec:
                            if phone in [ph for ph in rec['phones']]:
                                contacts.update_one({'name': name}, {'$pull': {'phones': phone}})
                                viewer("Phone deleted successfully")
                                break
                        else:
                            viewer("Number doesn't belong to the " + name + ". Try again")
                elif choose_p == 'o':
                    viewer("OK, let's go ahead")
                    break
                break
        elif choose == "o":
            viewer("OK, let's go ahead")
            break

    while True:
        viewer("Type 'E to edit e-mail,  'O' skip to other details")
        choose = input().lower()
        if choose == 'e':
            if 'email' in rec:
                viewer("Current email for the record " + name + " is:" + rec['email'])

            while True:
                viewer("Input email for the contact " + rec['name'])
                email = input()
                is_correct_format = re.search(r'[a-zA-Z0-9\.\-\_]+@[a-zA-Z0-9\-\_\.]+\.[a-z]{2,4}', email)
                if email == 'exit':
                    viewer("Operation cancelled")
                    break
                elif is_correct_format:
                    contacts.update_one({'name': name}, {'$set': {'email': email}})
                    viewer("Email successfully added")
                    break
                else:
                    viewer("Email should have format: 'name@domain.[domains.]high_level_domain'. "
                           "Incorrect email format. Try again or type 'Exit'")
            break
        if choose == 'o':
            viewer("OK, let's go ahead")
            break

    while True:
        viewer("Type 'A to edit  address,  'O'  skip to other details")
        choose = input().lower()
        rec = find_name(name)
        if choose == 'a':
            if 'address' in rec:
                viewer("Current saved address for record " + name + " is: " + rec['address'])
            viewer("Input address for the contact " + name)
            address = input("Input address: ")
            contacts.update_one({'name': name}, {'$set': {'address': address}})
            viewer("Address successfully added")
            break
        if choose == 'o':
            viewer("OK, let's go ahead")
            break

    while True:
        viewer("Type 'B' to edit birthday, 'F' to finish with contact")
        choose = input().lower()
        if choose == 'b':
            if 'birthday' in rec:
                viewer("Current birthday for record " + name + " is: " + str(rec['birthday'].date()))
            while True:
                viewer("Please enter the date of birthday in format dd.mm.yyyy")
                birthday = input().lower()
                is_correct_format = re.search(r'\d{2}.\d{2}.\d{4}', birthday)
                if birthday == 'exit':
                    viewer("Operation cancelled")
                    break
                elif is_correct_format:
                    try:
                        birthday = datetime.strptime(birthday, '%d.%m.%Y')
                        contacts.update_one({'name': name}, {'$set': {'birthday': birthday}})
                        viewer("Birthday set successfully")
                        break
                    except:
                        viewer('Date has incorrect format, please try again')
                        continue
                viewer("Date has incorrect format, please try again or type 'Exit' to come back to main menu")
            break
        if choose == 'f':
            break
    rec = find_name(name)
    redis_list.remove(name)
    viewer("Contact details saved")
    viewer(print_one(rec))
    return "How can I help you?"


def edit_name():
    while True:
        name = input().casefold()
        r = find_name(name)
        if r:
            while True:
                viewer("Type 'N' to edit a name, 'O' skip other details")
                choose = input().lower()
                if choose == 'n':
                    viewer("Please give me new name instead of : " + name)
                    name_new = input()

                    if not find_name(name_new):
                        contacts.update_one({'name': name}, {"$set": {"name": name_new}})
                        viewer("The name successfully changed")
                        return name_new
                    else:
                        viewer('Contact is already exist')
                        continue
                elif choose == 'o':
                    viewer("OK, let's go ahead")
                    return name

        elif name.lower() == 'exit':
            viewer("Operation cancelled")
            return "How can I help you?"
        else:
            viewer("Couldn't find this name in address book.")
            viewer("Please try to choose the name again or type 'Exit' to come back to main menu")


def edit_phones(rec):
    while True:
        phone = choose_phone()
        if phone == 'exit':
            return 0
        name = rec['name']
        if 'phone' in rec:
            if phone not in [ph for ph in rec['phones']]:
                try:
                    contacts.update_one({'name': name}, {'$push': {'phones': phone}})
                    viewer("Phone number successfully added")
                    return name
                except:
                    viewer("Incorrect phone format. Try again or type 'Exit'")
                    continue
            else:
                viewer("This number is already belong to contact " + name + ", please try again")
        else:
            contacts.update_one({'name': name}, {'$push': {'phones': phone}})
            viewer("Phone number successfully added")
            return name


def show_all(data):
    viewer("test of show all")
    users = find_all()
    for u in users:
        viewer(print_one(u))
    return "How can I help you?"


def print_one(rec):
    str_res = "      Name:          " + str(rec['name']) + "\n"
    if 'phones' in rec:
        str_res = str_res + "      Phone list:    "
        for p in rec['phones']:
            str_res = str_res + p + "\n                  "

        str_res = str_res[:-18]
    if 'email' in rec:
        str_res = str_res + "      Email:         " + str(rec['email']) + "\n"
    if 'address' in rec:
        str_res = str_res + "      Address:       " + str(rec['address']) + "\n"
    if 'birthday' in rec:
        str_res = str_res + "      Birthday:      " + str(rec['birthday'].date()) + "\n"
    str_res = str_res + "-----------------------------------------------------------"
    return str_res


def help_(command):
    viewer("List of available features: ")
    for key in exec_command.keys():
        viewer(exec_command[key][1])
    return "How can I help you?"


def choose_record():
    viewer("Please enter the name of a contact")
    while True:
        name = input().casefold()
        r = find_name(name)
        if r:
            break
        elif name.lower() == 'exit':
            break
        else:
            viewer("Couldn't find this name in address book.")
            viewer("Please try to choose the name again or type 'Exit' to come back to main menu")
    return name


def choose_phone():
    viewer("Please enter the phone number")
    while True:
        phone = input().lower()
        if phone == 'exit':
            break
        is_correct_format = re.search(r"\+?[\ \d\-\(\)]", phone)
        phone = sanitize_phone_number(phone)
        if is_correct_format and len(phone) == 13:
            break
        else:
            viewer("Phone should have format: '[+] [XX] XXXXXXXXXX' (10 or 12 digits). "
                   "Please try again or type 'Exit' to come back to main menu")
    return phone


def delete_contact(command):
    while True:
        name = choose_record()
        r = find_name(name)
        while True:
            viewer("Find a contact " + r['name'] + ", are you sure to delete it? Please type Y/N?")
            choose_d = input().lower()
            if choose_d == 'y':
                contacts.delete_one({'name': name})
                viewer("Contact " + name + " deleted")
                return "How can I help you?"
            elif choose_d == 'n':
                viewer("Operation cancelled")
                return "How can I help you?"
            else:
                viewer("Make a correct choice, please")
        return "How can I help you?"


def next_birthday(command):

    while True:
        res_lst = []
        viewer("How many days in the period we are looking for")
        days = input()
        try:
            period = int(days)
        except:
            viewer("Incorrect input, should be numeric between 0 and 365 days")
            continue
        if period > 365 or period <= 0:
            viewer("Incorrect, should be integer between 0 and 365 days")
            continue
        else:
            for person in find_all():
                if days_to_birthday(person) < period:
                    res_lst.append(person)
            if len(res_lst) > 0:
                viewer("List of contacts that have birthday in ", days, " days:")
                for res in res_lst:
                    viewer("Name ", res['name'], ", birthday ", str(res['birthday'].date()))
            else:
                viewer("I'm sorry, couldn't find any")
            break

    return "How can I help you?"


def days_to_birthday(person):
    current_date = datetime.now().date()
    if 'birthday' in person:
        birthday_date = person['birthday'].date().replace(year=current_date.year)
        delta = birthday_date - current_date
        if delta.days < 0:
            new_birthday_date = birthday_date.replace(year=birthday_date.year + 1)
            delta = new_birthday_date - current_date
            return delta.days
        else:
            delta = birthday_date - current_date
            return delta.days
    return 1000


def exit_func(data):
    viewer('Good bye!')


exec_command = {
    "help": [help_, "help:               Print a list of the available commands", 0],
    "hello": [hello_, "hello:              Greetings", 0],
    "add contact": [add_contact, "add contact:        Add a new contact", 2],
    "edit contact": [edit_contact, "edit contact:       Edit the contact detail", 2],
    "find contact": [find_contact, "find contact:       Find the record name", 1],
    "delete contact": [delete_contact, "delete contact:     Delete contact", 2],
    "next birthday": [next_birthday, "next birthday:      Let you the contacts with birthdays in specified period", 2],
    "show all contacts": [show_all, "show all contacts:  Print all the records of address book, page by page", 0],
    "exit": [exit_func, "exit:                Exits the program"]

}


def handler(command):
    if command == 'exit':
        return 'exit'
    else:
        return exec_command[command][0]("")


def listener():
    command = ""
    communication_str = "Hi! Looking for your order!"
    while communication_str not in exit_command:
        viewer(communication_str)
        message = input().lower()
        lev = process.extractOne(message, exec_command.keys())
        command = lev[0]
        communication_str = handler(command)


def start_bot():

    listener()


if __name__ == '__main__':
    start_bot()
