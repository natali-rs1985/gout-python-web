from clean import *
from notebook import *
from addressbook import *
from fuzzywuzzy import process
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

################################################################################
#         CLI BOT section                                                      #
################################################################################
exit_command = ["good bye", "close", "exit"]


def format_phone_number(func):
    def inner(phone):
        result = func(phone)
        if len(result) == 12:
            result = '+' + result
        else:
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


def add_phone(name):
    while True:
        phone = choose_phone()
        if phone == 'exit':
            return 0
        if phone not in [ph.value for ph in a.data[name].phones]:
            try:
                a.data[name].add_phone(Phone(phone, viewer))
                a.viewer("Phone number successfully added")
                return 1
            except:
                a.viewer("Incorrect phone format. Try again or type 'Exit'")
                continue
        else:
            a.viewer("This number already belonged to contact " + name + ", please try again")


def add_email(name):
    while True:
        a.viewer("Input email for the contact " + name)
        email = input()
        if email == 'exit':
            return 0
        else:
            try:
                a.data[name].add_email(Email(email, viewer))
                a.viewer("Email successfully added")
                return 1
            except:
                a.viewer("incorrect email format. Try again or type 'Exit'")
                continue


def add_address(name):
    address_dict = {}
    a.viewer("Input address for the contact " + name)
    address_dict["country"] = input("Input country: ")
    address_dict["zip"] = input("Input ZIP code: ")
    address_dict["region"] = input("Input region: ")
    address_dict["city"] = input("Input city: ")
    address_dict["street"] = input("Input street: ")
    address_dict["building"] = input("Input building: ")
    address_dict["apartment"] = input("Input apartment: ")
    a.data[name].add_address(Address(address_dict))
    a.viewer("Address successfully added")


def add_birthday(name):
    a.viewer("Please enter the date of birthday in format dd.mm.yyyy")
    birthday = input().lower()
    if birthday == 'exit':
        a.viewer("Operation cancelled")
    else:
        a.data[name].add_birthday(birthday)
        a.viewer("Birthday set successfully")
    return "How can I help you?"


def add_contact(data):
    '''
    add the record to address book
    :param data:
    :return:
    '''
    while True:
        a.viewer("Input the name of a contact")
        name = input()
        if name not in a.data.keys():
            r = Record(name, viewer)
            a.add_record(r)
            break
        else:
            a.viewer("Contact already exists. Try again")
    while True:
        a.viewer("Type 'P' to add phone, 'O' skip to other details")
        choose = input().lower()
        if choose == 'p':
            add_phone(name)
        if choose == 'o':
            a.viewer("OK, let's go ahead")
            break
    while True:
        a.viewer("Type 'E to enter e-mail, 'O' skip to other details")
        choose = input().lower()
        if choose == 'e':
            add_email(name)
            break
        if choose == 'o':
            a.viewer("OK, let's go ahead")
            break
    while True:
        a.viewer("Type 'A to enter address, 'O' skip to other details")
        choose = input().lower()
        if choose == 'a':
            add_address(name)
            break
        if choose == 'o':
            a.viewer("OK, let's go ahead")
            break
    while True:
        a.viewer("Type 'B' to enter birthday,'F' to finish")
        choose = input().lower()
        if choose == 'b':
            add_birthday(name)
            break
        if choose == 'f':
            break
    a.viewer("New contact details:")
    a.viewer(a.data[name])
    return "How can I help you?"


def edit_contact(data):
    '''
    edit the record in address book
    :param data:
    :return:
    '''
    name = choose_record()
    if name == 'exit':
        a.viewer("Operation cancelled")
        return "How can I help you?"

    while True:
        a.viewer("Type 'N' to edit a name, 'O' skip other details")
        choose = input().lower()
        if choose == 'n':
            a.viewer("Please let me new name: " + name)
            name_new = input()
            a.data[name_new] = a.data[name]
            a.data[name_new].name = Name(name_new)
            if name_new != name:
                a.data.pop(name)
            name = name_new
            a.viewer("The name successfully changed")
            break
        if choose == 'o':
            a.viewer("OK, let's go ahead")
            break

    while True:
        a.viewer("Type 'P' to edit phones, 'O' skip to other details")
        choose = input().lower()
        if choose == 'p':
            a.viewer("Existing phone numbers for the " + name)
            for ph in a.data[name].phones:
                a.viewer("      " + ph.value)
            while True:
                a.viewer("Type 'A' to add  phone, 'E' to edit, 'D' for delete, 'O' skip to other details")
                choose_p = input().lower()
                if choose_p == 'a':
                    add_phone(name)
                elif choose_p == 'e':
                    while True:
                        a.viewer("I need the old number to change")
                        phone = choose_phone()
                        if phone == 'exit':
                            a.viewer("Operation cancelled")
                            break
                        if phone in [ph.value for ph in a.data[name].phones]:
                            a.viewer("I need the new number to save")
                            phone_new = choose_phone()
                            a.data[name].edit_phone(phone, phone_new)
                            a.viewer("Phone changed successfully")
                        else:
                            a.viewer("This number doesn't belong to the " + name)
                            continue
                        break
                elif choose_p == 'd':
                    while True:
                        a.viewer("Input the number you would like to delete")
                        phone = choose_phone()
                        if phone == 'exit':
                            a.viewer("Operation cancelled")
                            break
                        elif phone in [ph.value for ph in a.data[name].phones]:
                            a.data[name].del_phone(phone)
                            a.viewer("Phone deleted successfully")
                            break
                        else:
                            a.viewer("Number doesn't belong to the " + name + ". Try again")
                elif choose_p == 'o':
                    a.viewer("OK, let's go ahead")
                    break
                break
        elif choose == "o":
            a.viewer("OK, let's go ahead")
            break

    while True:
        a.viewer("Type 'E to edit e-mail,  'O' skip to other details")
        choose = input().lower()
        if choose == 'e':
            if a.data[name].email:
                a.viewer("Current email for the record " + name + " is:" + a.data[name].email.value)
            add_email(name)
            break
        if choose == 'o':
            a.viewer("OK, let's go ahead")
            break

    while True:
        a.viewer("Type 'A to edit  address,  'O'  skip to other details")
        choose = input().lower()
        if choose == 'a':
            if a.data[name].address:
                a.viewer("Current saved address for record " + name + " is:")
                for key in a.data[name].address.value.keys():
                    a.viewer(" " * 12 + key + " " * (len("apartment") - len(key)) + ": " + a.data[name].address.value[
                        key])
            add_address(name)
            break
        if choose == 'o':
            a.viewer("OK, let's go ahead")
            break
    while True:
        a.viewer("Type 'B' to edit birthday, 'F' to finish with contact")
        choose = input().lower()
        if choose == 'b':
            if a.data[name].birthday:
                a.viewer("Current birthday for record " + name + " is: " + a.data[name].birthday.value
                         .strftime("%m/%d/%Y"))
            add_birthday(name)
            break
        if choose == 'f':
            break
    a.viewer("Contact details saved")
    a.viewer(a.data[name])
    return "How can I help you?"


def find_contacts(data):
    res_lst = []
    a.viewer("Please input the name, phone or even a part of them")
    search_str = input().rstrip()
    search_str = (
        search_str.strip()
            .replace("+", "\+")
            .replace("*", "\*")
            .replace("{", "\{")
            .replace("}", "\}")
            .replace("[", "\[")
            .replace("]", "\]")
            .replace("?", "\?")
            .replace("$", "\$")
            .replace("'\'", "\\")

    )
    res_lst = a.find(search_str)
    if len(res_lst) == 0:
        a.viewer("Couldn't find records in the phone book")
    else:
        a.viewer("Found next contacts:")
        for contact in res_lst:
            a.viewer(a.data[contact])
    return "How can I help you?"


def show_all(data):
    a.viewer("test of show all")
    adress_book = a
    for page in adress_book:
        for record in page:
            a.viewer(a.data[record["Name"]])
        input("Press enter to continue")
    return "How can I help you?"


def help_(command):
    a.viewer("List of available features: ")
    for key in exec_command.keys():
        a.viewer(exec_command[key][1])
    return "How can I help you?"


def choose_record():
    a.viewer("Please enter the name of a contact")
    while True:
        name = input()
        if name.lower() in [x.lower() for x in a.data.keys()]:
            for key in a.data.keys():
                if name.lower() == key.lower():
                    name = key
            break
        elif name.lower() == 'exit':
            break
        else:
            a.viewer("Couldn't find this name in address book.")
            a.viewer("Here are the list of the contacts with similar spelling:")
            for c in a.find(name):
                a.viewer("     " + c)
            a.viewer("Please try to choose the name again or type 'Exit' to come back to main menu")
    return name


def choose_phone():
    a.viewer("Please enter the phone number")
    while True:
        phone = input().lower()
        if phone == 'exit':
            break
        is_correct_format = re.search("\+?[\ \d\-\(\)]+$", phone)
        phone = sanitize_phone_number(phone)
        if is_correct_format and len(phone) == 13:
            break
        else:
            a.viewer("Phone number is incorrect format, please try again or type 'Exit' to come back to main menu")
    return phone


def choose_date():

    while True:
        birthday = input().lower()
        is_correct_format = re.search("\d{2}[\/\.\:]\d{2}[\/\.\:]\d{4}", birthday)
        if is_correct_format:
            birthday = birthday.replace("/", ".")
            birthday = birthday.replace(":", ".")
            b_array = birthday.split(".")
            try:
                datetime.strptime(birthday, '%d.%m.%Y').date()
            except ValueError:
                a.viewer("You gave me incorrect date, be careful nex time")
            else:
                break
        elif birthday == 'exit':
            break
        a.viewer("Date has incorrect format, please try again or type 'Exit' to come back to main menu")
    return birthday


def delete_contact(command):
    choose = ""
    while True:
        name = choose_record()
        while True:
            a.viewer("Find a contact " + name + ", are you sure to delete it? Please type Y/N?")
            choose_d = input().lower()
            if choose_d == 'y':
                a.delete(name)
                a.viewer("Contact " + name + " deleted")
                return "How can I help you?"
            elif choose_d == 'n':
                a.viewer("Operation cancelled")
                return "How can I help you?"
            else:
                a.viewer("Make a correct choice, please")
        return "How can I help you?"


def add_note(command):
    '''
    add the note to note book
    :param command:
    :return:
    '''
    while True:
        n.viewer(
            "Input the text of your note here. Use a hashtags # for key_words. Allowed to use copy/paste to speed up")
        note = Note(input())
        if len(note.keyword) == 0:
            n.viewer("You forgot to add a keywords, please let me them, using # and separate them by spaces")
            input_str = input("#Key words: ")
            lst = input_str.split(" ")
            for kw in lst:
                note.keyword.append(kw[1:])
        n.add_note(note)
        break

    return "How can I help you?"


def edit_note(command):
    """
    edit the note
    :param command:
    :return:
    """
    while True:
        n.viewer("""Input the keywords for the note you would like to edit 
        (You could input a couple of keywords separated by spaces)""")
        input_str = input()
        res_lst = n.find(input_str)
        if res_lst:
            n.viewer("I found some notes connected to your request:")
            for result in res_lst:
                n.viewer(result)
            break
        elif input_str.lower() == 'exit':
            n.viewer("Operation cancelled")
            return 0
        else:
            n.viewer("Couldn't find notes with specified keywords, try again or type 'exit'")
            continue
    while True:
        choose = input("Input ID of note you would like to edit: ")
        if choose in [str(x.id) for x in res_lst]:
            n.viewer("Keywords: ", ["# " + k for k in n.data[int(choose)].keyword])
            n.viewer("----------------- you could copy here ------------------------")
            n.viewer(n.data[int(choose)].note)
            n.viewer("------------------ avoid new line character when copy --------")
            n.viewer("You could use copy/paste to speed up. Use # to mark up keywords")
            new_text = input()
            note_temp = Note(new_text)
            n.viewer("Please add a keywords for a note, separated by space.")
            kw_lst = input("Keywords: ").split(" ")
            n.viewer(kw_lst)
            note_temp.keyword.extend(kw_lst)
            n.data[int(choose)] = note_temp
            n.viewer("Note successfully changed")
            break
        elif choose.lower() == 'exit':
            n.viewer("Operation cancelled")
            break
        else:
            n.viewer("Make a correct choice")
            continue
        break

    return "How can I help you?"


def delete_note(command):
    """
    delete the note
    :param command:
    :return:
    """
    while True:
        res_lst = []
        n.viewer("Input the keyword for the note you would like to delete")
        input_str = input("You could input a couple of keywords separated by spaces: ")
        res_lst = n.find(input_str)
        if len(res_lst) > 0:
            n.viewer("I found some notes connected to your request:")
            for result in res_lst:
                n.viewer(result)
            while True:
                choose = input("Input ID of note you would like to delete: ")
                if choose in [str(x.id) for x in res_lst]:
                    n.delete(int(choose))
                    n.viewer("Note successfully deleted")
                    break
                elif choose.lower() == 'exit':
                    n.viewer("Operation cancelled")
                    break
                else:
                    n.viewer("Make a correct choice")
                    continue
            break

        elif input_str.lower() == 'exit':
            n.viewer("Operation cancelled")
            break

        else:
            n.viewer("Couldn't find notes with specified keywords, try again or type 'exit'")
            continue
    return "How can I help you?"


def find_notes(command):
    while True:
        res_lst = []
        n.viewer("Input the keyword for the note you would like to find")
        input_str = input("Allowed input of multiply keywords separated by spaces: ")
        res_lst = n.find(input_str)
        if len(res_lst) > 0:
            n.viewer("I found some notes connected to your request:")
            for result in res_lst:
                n.viewer(result)
            break
        elif input_str.lower() == 'exit':
            n.viewer("Operation cancelled")
            break
        else:
            n.viewer("Couldn't find notes with specified keywords, try again or type 'exit'")
            continue
    return "How can I help you?"


def show_notes(command):
    """
    show all the notes
    :param command:
    :return:
    """
    for page in n:
        for record in page:
            n.viewer(record)
        input("Press enter to continue")
    return "How can I help you?"


def sort_notes(command):
    """
    sorting the notes by keywords list
    :param command:
    :return:
    """
    sort_notebook = Notebook("temp", viewer)
    sort_notebook.data = dict(sorted(n.data.items(), key=lambda item: sorted(item[1].keyword, key=lambda x: x.upper())))
    n.data = sort_notebook.data
    for item in n.data.keys():
        n.data[item].keyword = sorted(n.data[item].keyword, key=lambda x: x.upper())
        n.viewer(n.data[item])
    n.viewer("Sorting completed")
    return "How can I help you?"


def sort_folder(command):
    """
    add code of sorting function here
    :param command:
    :return:
    """
    while True:
        a.viewer("Type path to the folder, use '/' to folders")
        path = Path(input())
        if path.exists():
            parse_folder(path)
            break
        else:
            a.viewer("Path doesn't exist")
    a.viewer("Sorting completed")
    return "How can I help you?"


################################################################################################################

def next_birthday(command):

    while True:
        res_lst = []
        a.viewer("How many days in the period we are looking for")
        days = input()
        try:
            period = int(days)
        except:
            a.viewer("Incorrect input, should be numeric between 0 and 365 days")
            continue
        if period > 365 or period <= 0:
            a.viewer("Incorrect, should be integer between 0 and 365 days")
            continue
        else:
            for person in a.data.values():
                if person.days_to_birthday() < period:
                    res_lst.append(person)
            if len(res_lst) > 0:
                a.viewer("List of contacts that have birthday in ", days, " days:")
                for res in res_lst:
                    a.viewer("Name ", res.name.value, ", birthday ", str(res.birthday.value))
            else:
                a.viewer("I'm sorry, couldn't find any")
            break

    return "How can I help you?"


def save_(data):
    a.dump("Work_telephones.json")
    n.dump("Work_notes.json")
    a.viewer("All data saved")
    return "How can I help you?"


def exit_func(data):
    a.viewer('Good bye!')


exec_command = {
    "hello": [hello_, "hello:              Greetings", 0],
    "add contact": [add_contact, "add contact:        Add a new contact", 2],
    "edit contact": [edit_contact, "edit contact:       Edit the contact detail", 2],
    "find contact": [find_contacts, "find contact:       Find the records by phone or name", 1],
    "find notes": [find_notes, "find notes:         Find the notes by text or keywords", 1],
    "show all contacts": [show_all, "show all contacts:  Print all the records of adress book, page by page", 0],
    "show all notes": [show_notes, "show all notes:     Print all the records of adress book, page by page", 0],
    "help": [help_, "help:               Print a list of the available commands", 0],
    "add note": [add_note, "add note:           Add new text note ", 0],
    "edit note": [edit_note, "edit note:          Edit existing text note ", 0],
    "delete contact": [delete_contact, "delete contact:     Delete contact", 2],
    "delete note": [delete_note, "delete note:        Delete text note", 2],
    "sort notes": [sort_notes, "sort note:          Sort of the notes by keywords", 2],
    "sort folder": [sort_folder, "sort folder:        Sort selected folder by file types", 2],
    "next birthday": [next_birthday, "next birthday:      Let you the contats with birthdays in specified period", 2],
    "save": [save_, "save:               Save the current state of data to disk", 0],
    "exit": [exit_func, "exit:                Exits the program"]

}


def handler(command):
    if command == 'exit':
        return 'exit'
    else:
        return exec_command[command][0]("")


viewer = ViewerInterface().view
a = AddressBook("Work telephones", viewer)
n = Notebook("Work notes", viewer)


def listener():
    command = ""
    communication_str = "Hi! Looking for your order!"
    while communication_str not in exit_command:
        a.viewer(communication_str)
        message = input().lower()
        leven = process.extractOne(message, exec_command.keys())
        command = leven[0]
        communication_str = handler(command)
        save_(None)


def start_bot():
    # a.load("Work_telephones.json")
    try:
        a.load("Work_telephones.json")
    except:
        a.viewer("Couldn't find file, starting with empty address book")
    try:
        n.load("Work_notes.json")
    except:
        a.viewer("Couldn't load file, starting with empty note book")
    listener()
    try:
        a.dump("Work_telephones.json")
        n.dump("Work_notes.json")
    except:
        a.viewer("Couldn't save file, all the changes could be loose")


start_bot()
