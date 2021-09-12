from models import *
from fuzzywuzzy import process
import warnings
from load import *


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


def add_phone(r):
    while True:
        phone = choose_phone()
        if phone == 'exit':
            return 0
        if phone not in [ph.phone for ph in r.phones]:
            try:
                r.add_phone(phone)
                viewer("Phone number successfully added")
                return 1
            except:
                viewer("Incorrect phone format. Try again or type 'Exit'")
                continue
        else:
            viewer("This number already belonged to contact " + str(r.username) + ", please try again")


def add_email(r):
    while True:
        viewer("Input email for the contact " + str(r.username))
        email = input()
        is_correct_format = re.search(r'[a-zA-Z0-9\.\-\_]+@[a-zA-Z0-9\-\_\.]+\.[a-z]{2,4}', email)
        if email == 'exit':
            return 0
        elif is_correct_format:
            if r.email:
                new_email = session.query(Email).filter(Email.email_id == r.email_id).first()
                new_email.email = email
                session.commit()
            else:
                r.add_email(email)
            viewer("Email successfully added")
            return 1
        else:
            viewer("Email should have format: 'name@domain.[domains.]high_level_domain'. "
                   "Incorrect email format. Try again or type 'Exit'")


def add_address(r):
    viewer("Input address for the contact " + str(r.username))
    address = input("Input address: ")
    if r.address:
        old_address = session.query(Address).filter(Address.address_id == r.address_id).first()
        old_address.address = address
        session.commit()
    else:
        r.add_address(address)
    viewer("Address successfully added")


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
                birthday = datetime.strptime(birthday, '%d.%m.%Y').date()
                if r.birthday:
                    old_birthday = session.query(Birthday).filter(Birthday.birthday_id == r.birthday_id).first()
                    old_birthday.birthday = birthday
                    session.commit()
                else:
                    r.add_birthday(birthday)
                viewer("Birthday set successfully")
                break
            except:
                print('Date has incorrect format, please try again')
                continue
        viewer("Date has incorrect format, please try again or type 'Exit' to come back to main menu")
    return "How can I help you?"


def find_name(name):
    name = session.query(Record).join(Record.username).filter(Name.username == name).first()
    return name


def find_all():
    users = session.query(Record).all()
    return users


def add_contact(data):

    while True:
        viewer("Input the name of a contact")
        r = input()
        find = find_name(r)
        if not find:
            n = Name(r)
            session.add(n)
            session.commit()
            r = Record(n)
            session.add(r)
            session.commit()
            break
        else:
            viewer("Contact already exists. Try again")

    while True:
        viewer("Type 'P' to add phone, 'O' skip to other details")
        choose = input().lower()
        if choose == 'p':
            add_phone(r)
        if choose == 'o':
            viewer("OK, let's go ahead")
            break

    while True:
        viewer("Type 'E to enter e-mail, 'O' skip to other details")
        choose = input().lower()
        if choose == 'e':
            add_email(r)
            break
        if choose == 'o':
            viewer("OK, let's go ahead")
            break

    while True:
        viewer("Type 'A to enter address, 'O' skip to other details")
        choose = input().lower()
        if choose == 'a':
            add_address(r)
            break
        if choose == 'o':
            viewer("OK, let's go ahead")
            break

    while True:
        viewer("Type 'B' to enter birthday,'F' to finish")
        choose = input().lower()
        if choose == 'b':
            add_birthday(r)
            break
        if choose == 'f':
            break
    viewer("New contact details:")
    viewer(r)
    return "How can I help you?"


def edit_contact(data):
    viewer("Please enter the name of a contact")
    r = edit_name()

    while True:
        viewer("Type 'P' to edit phones, 'O' skip to other details")
        choose = input().lower()
        if choose == 'p':
            viewer("Existing phone numbers for the " + str(r.username))
            for ph in r.phones:
                viewer("      " + str(ph))
            while True:
                viewer("Type 'A' to add  phone, 'E' to edit, 'D' for delete, 'O' skip to other details")
                choose_p = input().lower()
                if choose_p == 'a':
                    add_phone(r)
                elif choose_p == 'e':
                    while True:
                        viewer("I need the old number to change")
                        phone = choose_phone()
                        if phone == 'exit':
                            viewer("Operation cancelled")
                            break
                        if phone in [ph.phone for ph in r.phones]:
                            viewer("I need the new number to save")
                            phone_new = choose_phone()
                            r.edit_phone(phone, phone_new)
                            viewer("Phone changed successfully")
                        else:
                            viewer("This number doesn't belong to the " + str(r.username))
                            continue
                        break
                elif choose_p == 'd':
                    while True:
                        viewer("Input the number you would like to delete")
                        phone = choose_phone()
                        if phone == 'exit':
                            viewer("Operation cancelled")
                            break
                        elif phone in [ph.phone for ph in r.phones]:
                            r.del_phone(phone)
                            viewer("Phone deleted successfully")
                            break
                        else:
                            viewer("Number doesn't belong to the " + str(r.username) + ". Try again")
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
            if r.email:
                viewer("Current email for the record " + str(r.username) + " is:" + str(r.email))
            add_email(r)
            break
        if choose == 'o':
            viewer("OK, let's go ahead")
            break

    while True:
        viewer("Type 'A to edit  address,  'O'  skip to other details")
        choose = input().lower()
        if choose == 'a':
            if r.address:
                viewer("Current saved address for record " + str(r.username) + " is: " + str(r.address))
            add_address(r)
            break
        if choose == 'o':
            viewer("OK, let's go ahead")
            break

    while True:
        viewer("Type 'B' to edit birthday, 'F' to finish with contact")
        choose = input().lower()
        if choose == 'b':
            if r.birthday:
                viewer("Current birthday for record " + str(r.username) + " is: " + str(r.birthday))
            add_birthday(r)
            break
        if choose == 'f':
            break
    viewer("Contact details saved")
    viewer(r)
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
                    user_name = session.query(Name).filter(Name.name_id == r.name_id).first()
                    user_name.username = name_new
                    session.commit()
                    viewer("The name successfully changed")
                    return r
                elif choose == 'o':
                    viewer("OK, let's go ahead")
                    return r

        elif name.lower() == 'exit':
            viewer("Operation cancelled")
            return "How can I help you?"
        else:
            viewer("Couldn't find this name in address book.")
            viewer("Please try to choose the name again or type 'Exit' to come back to main menu")


def find_contacts(data):
    viewer("Please input the name")
    search_str = input().rstrip()
    res = session.query(Record).join(Record.username).filter(Name.username == search_str).first()
    if not res:
        viewer("Can't find record in the phone book")
    else:
        viewer("Found contact:")
        viewer(res)
    return "How can I help you?"


def show_all(data):
    viewer("test of show all")
    users = find_all()
    for u in users:
        viewer(u)
    return "How can I help you?"


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
            viewer("Find a contact " + str(r.username) + ", are you sure to delete it? Please type Y/N?")
            choose_d = input().lower()
            if choose_d == 'y':
                session.delete(r)
                viewer("Contact " + str(r.username) + " deleted")
                session.commit()
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
                if person.days_to_birthday() < period:
                    res_lst.append(person)
            if len(res_lst) > 0:
                viewer("List of contacts that have birthday in ", days, " days:")
                for res in res_lst:
                    viewer("Name ", str(res.username), ", birthday ", str(res.birthday))
            else:
                viewer("I'm sorry, couldn't find any")
            break

    return "How can I help you?"


def exit_func(data):
    viewer('Good bye!')


exec_command = {
    "help": [help_, "help:               Print a list of the available commands", 0],
    "hello": [hello_, "hello:              Greetings", 0],
    "add contact": [add_contact, "add contact:        Add a new contact", 2],
    "edit contact": [edit_contact, "edit contact:       Edit the contact detail", 2],
    "find contact": [find_contacts, "find contact:       Find the record name", 1],
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
