from clean import *
from notebook import *
from addressbook import *
from fuzzywuzzy import process
import warnings 
warnings.filterwarnings('ignore')



################################################################################
#         CLI BOT section                                                      #
################################################################################

exit_command = ["good bye", "close", "exit"]


def format_phone_number(func):
   def inner(phone):
      result=func(phone)
      if len(result) == 12:
          result='+'+result
      else: result='+38'+result    
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
               a.data[name].add_phone(Phone(phone))
               print ("Phone number succesfully added")
               return 1
            except:
               print("incorrect phone format. Try again or type 'Exit'")
               continue
        else:
            print("This number already belonged to contact "+name+", please try again")

def add_email(name):
    while True:
        print("Input email for the contact "+name)
        email = input()
        if email == 'exit':
            return 0 
        else:
            try:
                a.data[name].add_email(Email(email))
                print ("Email succesfully added")
                return 1
            except:
                print("incorrect email format. Try again or type 'Exit'")
                continue
            
        

def add_address(name):
    address_dict = {}
    print("Input address for the contact "+name)
    address_dict["country"] = input("Input country: ")
    address_dict["zip"] = input("Input ZIP code: ")
    address_dict["region"] = input("Input region: ")
    address_dict["city"] = input("Input city: ")
    address_dict["street"] = input("Input street: ")
    address_dict["building"] = input("Input building: ")
    address_dict["apartment"] = input("Input apartment: ")
    a.data[name].add_address(Address(address_dict))
    print ("Address succesfully added")
            

def add_birthday(name):
    birthday = choose_date()
    if birthday == 'exit':
        print("Operation canselled")
    else:
        b=Birthday(birthday)
        a.data[name].add_birthday(b)
        print("Birthday setted successfully")
    return "How can I help you?"
            

############################# add the record to address book ####################################################
 
def add_contact(data):
    while True:
        print("Input the name of a contact")
        name = input()
        if name not in a.data.keys():
            r = Record(name)
            a.add_record(r)
            break
        else:
            print("Contact already exists. Try again")
    while True:
        print("Type 'P' to add phone, 'O' skip to other details")
        choose = input().lower()
        if choose =='p':
            add_phone(name)
        if choose == 'o':
            print("OK, let's go ahead")
            break
    while True:
        print("Type 'E to enter e-mail, 'O' skip to other details")
        choose = input().lower()
        if choose =='e':
            add_email(name)
            break
        if choose == 'o':
            print("OK, let's go ahead")
            break
    while True:
        print("Type 'A to enter address,  'O' skip to other details")
        choose = input().lower()
        if choose =='a':
            add_address(name)
            break
        if choose == 'o':
            print("OK, let's go ahead")
            break
    while True:
        print("Type 'B' to enter birthday,'F' to finish")
        choose = input().lower()
        if choose =='b':
            add_birthday(name)
            break
        if choose == 'f':
            break
    print("New contact details:")
    print(a.data[name])
    return "How can I help you?" 


############################# edit the record in address book ####################################################

def edit_contact(data):
    name = choose_record()
    if name == 'exit':
        print("Operation canselled")
        return "How can I help you?"

    while True:
        print("Type 'N' to edit a name, 'O' skip other details")
        choose = input().lower()
        if choose =='n':
            print("Please let me new name: "+name)
            name_new = input()
            a.data[name_new] = a.data[name]
            a.data[name_new].name=Name(name_new)
            a.data.pop(name)
            name = name_new
            print("The name succesfully changed")
            break 
        if choose == 'o':
            print("OK, let's go ahead")
            break
    while True:
        print("Type 'P' to edit phones, 'O' skip to other details")
        choose = input().lower()
        if choose =='p':
            print("Existing phone numbers for the "+name)
            for ph in a.data[name].phones:
                print("      "+ph.value)
            while True:
                print("Type 'A' to add  phone, 'E' to edit, 'D' for delete, 'O' skip to other details")
                choose_p = input().lower()
                if choose_p == 'a':
                     add_phone(name)
                elif choose_p == 'e':
                    while True:
                        print("I need the old number to change")
                        phone = choose_phone()
                        if phone == 'exit':
                            print("Operation canselled")
                            break
                        if phone in [ph.value for ph in a.data[name].phones]:
                            print("I need the new number to save")
                            phone_new = choose_phone()
                            a.data[name].edit_phone(phone, phone_new)
                            print ("Phone changed succesfully")
                        else:
                            print("This number doesn't belong to the "+name)
                            continue
                        break
                elif choose_p == 'd':
                    while True:
                        print("input the number you would like to delete")
                        phone = choose_phone()
                        if phone == 'exit':
                            print("Operation canselled")
                            break
                        elif phone in [ph.value for ph in a.data[name].phones]:
                            a.data[name].del_phone(phone)
                            print ("Phone deleted succesfully")
                            break
                        else:
                            print("Number doesn't belong to the "+name+" Try again")
                elif choose_p == 'o':
                    print("OK, let's go ahead")
                    break
                break
        elif choose == "o":
            print("OK, let's go ahead")
            break
    while True:
        print("Type 'E to edit e-mail,  'O' skip to other details")
        choose = input().lower()
        if choose =='e':
            if type(a.data[name].email)!=type(""):
                print("Current email for the record "+name+" is:"+a.data[name].email.value) 
            add_email(name)
            break
        if choose == 'o':
            print("OK, let's go ahead")
            break
    while True:
        print("Type 'A to edit  address,  'O'  skip to other details")
        choose = input().lower()
        if choose =='a':
            if type(a.data[name].address)!=type(""):
                print ("Current saved address for record "+name+" is:")
                for key in record["address"].keys():
                    print("            "+key+" "*(len("apartment")-len(key))+": "+record["address"][key])

            add_address(name)
            break
        if choose == 'o':
            print("OK, let's go ahead")
            break
    while True:
        print("Type 'B' to edit birthday, 'F' to finish with contact")
        choose = input().lower()
        if choose =='b':
            if type(a.data[name].address)!=type(""):
                print ("Current birthday for record "+name+" is: "+a.data[name].birthday.value)
            add_birthday(name)
            break
        if choose == 'f':
            break    
    print("Contact details saved")
    print(a.data[name])
    return "How can I help you?"
  

def find_contacts(data):
    res_lst =[]
    print("Please input the name, phone or even a part of them")
    search_str = input().rstrip()
    search_str = (
        search_str.strip()
            .replace("+","\+")
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
    if res_lst == []:
        print("Couldn't find records in the phone book")
    else:
        print("Found next contacts:")
        for contact in res_lst:
            print(a.data[contact])
    return "How can I help you?"

def show_all(data):
    print("test of show all")    
    adress_book = a    
    for page in adress_book:
        for record in page:
            print(a.data[record["Name"]])
        input("Press enter to continue")
    return "How can I help you?"

def help_(command):
    print("List of available features: ")
    for key in exec_command.keys():
        print (exec_command[key][1])
    print ("exit:      Exit program ('good by', 'close' also works)")    
    return "How can I help you?"



def choose_record():
    print("Please enter the name of a contact")
    while True:
        name = input()
        if name.lower() in [x.lower() for x in a.data.keys()]:
            for key in   a.data.keys():
                if name.lower() == key.lower():
                    name = key
            break
        elif name.lower() == 'exit':
            break
        else:
            print("Couldn`t find this name in adress book.")
            print("Here are the list of the contacts with similar spelling:")
            for c in a.find(name):
                print("     "+c)
            print("Please try to choose the name again or type 'Exit' to come back to main menu")    
    return name

def choose_phone():
    print("Please enter the phone number")
    while True:
        phone = input().lower()
        if phone == 'exit':
            break
        is_correct_format= re.search("\+?[\ \d\-\(\)]+$",phone)
        phone= sanitize_phone_number(phone)
        if is_correct_format!=None and len(phone) == 13: 
            break
        else:
            print("Phone number is incorrect format, please try again or type 'Exit' to come back to main menu")
    return phone

def choose_date():
    print("Please enter the date of birthday in format dd.mm.yyyy")
    while True:
        birthday = input().lower()
        is_correct_format= re.search("\d{2}[\/\.\:]\d{2}[\/\.\:]\d{4}",birthday)
        if is_correct_format!=None:
            birthday = birthday.replace("/",".")
            birthday = birthday.replace(":",".")
            b_array = birthday.split(".")
            try:
                datetime.strptime(birthday, '%d.%m.%Y').date()
            except ValueError:
                print("You gave me incorrect date, be carefull nex time")
            else:
                break
        elif birthday == 'exit':
            break
        print("Date has incorrect format, please try again or type 'Exit' to come back to main menu")
    return birthday


def delete_contact(command):
    choose = ""
    while True:
        name = choose_record()
        while True:
            print ("Find a contact "+name+", are you sure to delete it? Please type Y/N?")
            choose_d = input().lower()
            if choose_d == 'y': 
                a.delete(name)
                print("Contact "+name+" deleted")
                return "How can I help you?"
            elif choose_d == 'n':
                print("Operation canselled")
                return "How can I help you?"
            else:
                print("Make a correct choise, please")
        return  "How can I help you?"         

############################# add the note to note book ####################################################
def add_note(command):
    while True:
        print("Input the text of your note here. Use a hashtags # for key_words. Allowed to use copy/paste to speed up" )
        note = Note(input())
        if len(note.keyword) ==0:
            print("You forgot to add a keywords, please let me them, using # and separate them by spaces")
            input_str = input("#Key words: ")
            lst = input_str.split(" ")
            for kw in lst:
                note.keyword.append(kw[1:])
        n.add_note(note)        
        break
        
    return "How can I help you?"

############################# edit the note  ####################################################
def edit_note(command):
    while True:
        res_lst=[]
        print("Input the keywords for the note you would like to edit (You could input a couple of keywords separated by spaces)" )
        input_str=input()
        res_lst=n.find(input_str)
        if res_lst!=[]:
            print("I found some notes connected to your request:")
            for result in res_lst:
                print(result)
            break                   
        elif input_str.lower() == 'exit':
            print("Operation canselled")
            return 0
        else:
            print("Couldn't find notes with specified keywords, try again or type 'exit'")
            continue       
    while True:
        choose = input("Input ID of note you would like to edit: ")
        if  choose in [str(x.id) for x in res_lst]:
            print("Keywords: ",["# "+k for k in n.data[int(choose)].keyword])
            print("----------------- you could copy here ------------------------")
            print(n.data[int(choose)].note)    
            print("------------------ avoid new line character when copy --------")
            print("You could use copy/paste to speed up. Use # to mark up keywords")
            new_text = input()
            note_temp = Note(new_text)
            print("Please add a keywords for a note, separated by space.")
            kw_lst=input("Keywords: ").split(" ")
            print(kw_lst)
            note_temp.keyword.extend(kw_lst)
            n.data[int(choose)] = note_temp
            print("Note succesfully changed")
            break
        elif choose.lower() == 'exit':
            print("Operation cancelled")
            break
        else:
            print("Make a correct choice")
            continue
        break

           
    return "How can I help you?"

############################# delete the note ####################################################
def delete_note(command):
    while True:
        res_lst=[]
        print("Input the keyword for the note you would like to delete" )
        input_str=input("You could input a couple of keywords separated by spaces: ")
        res_lst = n.find(input_str)    
        if len(res_lst)!=0:
            print("I found some notes connected to your request:")
            for result in res_lst:
                print(result)
            while True:
                choose = input("Input ID of note you would like to delete: ")
                if  choose in [str(x.id) for x in res_lst]:
                    n.delete(int(choose))
                    print("Note succesfully deleted")
                    break
                elif choose.lower() == 'exit':
                    print("Operation cancelled")
                    break
                else:
                    print("Make a correct choice")
                    continue
            break

        elif input_str.lower() == 'exit':
            print("Operation cancelled")
            break
        
        else:
            print("Couldn't find notes with specified keywords, try again or type 'exit'")
            continue
    return "How can I help you?"


def find_notes(command):
    while True:
        res_lst=[]
        print("Input the keyword for the note you would like to find" )
        input_str=input("Allowed input of multiply keywords separated by spaces: ")
        res_lst=n.find(input_str)   
        if len(res_lst)!=0:
            print("I found some notes connected to your request:")
            for result in res_lst:
                print(result)
            break
        elif input_str.lower() == 'exit':
            print("Operation cancelled")
            break
        else:
            print("Couldn't find notes with specified keywords, try again or type 'exit'")
            continue
    return "How can I help you?"



############################# show all the notes ####################################################
def show_notes(command):
    for page in n:
        for record in page:
            print(record)
        input("Press enter to continue")
    return "How can I help you?"


############################# sorting the notes by keywords list ####################################################
def sort_notes(command):
    sort_notebook = Notebook("temp")
    sort_notebook.data = dict(sorted(n.data.items(), key=lambda item: sorted(item[1].keyword, key = lambda x: x.upper())))
    n.data = sort_notebook.data
    for item in n.data.keys():
        n.data[item].keyword =  sorted(n.data[item].keyword, key = lambda x: x.upper())   
        print(n.data[item])
    print("Sorting completed")
    return "How can I help you?"


############           add code of sorting function here ######################################################
def sort_folder(command):
    while True: 
        print("Type path to the folder, use '/' to folders")
        path = Path(input())
        if path.exists(): 
            parse_folder(path)
            break 
        else:
            print("Path doesn`t exist")    
    print("Sorting completed")
    return "How can I help you?"


################################################################################################################

def next_birthday(command):
    res_lst = []
    while True:    
        print("How many days in the period we are looking for")
        days = input()
        try:
            period = int(days)
            if period >365 or period <=0:
                print("Incorrect, should be integer between 0 and 365 days")
                continue
            else:
                for name in a.data.keys():
                   if int(a.data[name].days_to_birthday())<period:
                       res_lst.append(a.data[name])
                if len(res_lst)>0:
                    print("List of contacts that have birthday in ", days," days:")
                    for res in res_lst:
                        print("Name ", res.name.value, ", birthday ",str(res.birthday.value))
                else:
                    print("I'm sorry, couldn't find any")
                break
        except:
            print("Incorrect input, should be numeric between 0 and 365 days")
            continue
    return "How can I help you?"



def save_(data):
    a.dump("Work telephones.json")
    n.dump("Work notes.json")
    print("All data saved")
    return "How can I help you?"
    
exec_command = { 
    "hello": [hello_,                  "hello:              Greetings", 0], 
    "add contact":  [add_contact,      "add contact:        Add a new contact", 2], # adopted to the project needs
    "edit contact": [edit_contact,     "edit contact:       Edit the contact detail", 2], # adopted to the project needs
    "find contact": [find_contacts,    "find contact:       Find the records by phone or name", 1], # adopted to the project needs
    "find notes":   [find_notes,       "find notes:         Find the notes by text or keywords", 1], # adopted to the project needs
    "show all contacts": [show_all,    "show all contacts:  Print all the records of adress book, page by page", 0], # adopted to the project needs
    "show all notes":    [show_notes,  "show all notes:     Print all the records of adress book, page by page", 0], # adopted to the project needs
    "help": [help_,                    "help:               Print a list of the available commands",0],  # adopted to the project needs,
    "add note": [add_note,             "add note:           Add new text note ", 0],# adopted to the project needs
    "edit note": [edit_note,           "edit note:          Edit existing text note ", 0],# adopted to the project needs
    "delete contact": [delete_contact, "delete contact:     Delete contact", 2], # adopted to the project needs,
    "delete note": [delete_note,       "delete note:        Delete text note", 2], # adopted to the project needs,
    "sort notes": [sort_notes,         "sort note:          Sort of the notes by keywords", 2], # adopted to the project needs
    "sort folder": [sort_folder,       "sort folder:        Sort selected folder by file types", 2], # adopted to the project needs
    "next birthday": [next_birthday,   "next birthday:      Let you the contats with birthdays in specified period", 2], # adopted to the project needs
    "save": [save_,                    "save:               Save the current state of data to disk", 0]  # adopted to the project needs,
                           
             }


def handler(command):
    if command == 'exit':
        return 'exit'
    else:
        return exec_command[command][0]("")
          
def listener():
    command = ""
    communication_str = "Hi! Looking for your order!"
    while (communication_str) not in exit_command:
        print(communication_str)
        message = input().lower()
        a = process.extractne(message, exec_command.keys())
        command = a[0]
        communication_str = handler(command)

a = AddressBook("Work telephones")
n = Notebook("Work notes")

def start_bot():
   try:
      a.load("Work telephones.json")
   except:
      print("Couldn't find file, starting with empty adress book")
   try:
      n.load("Work notes.json")    
   except:
      print("Couldn't load file, starting with empty note book")
   listener() 
   try:
      a.dump("Work telephones.json")
      n.dump("Work notes.json")
   except:
      print("Couldn't save file, all the changes could be loose")

start_bot()