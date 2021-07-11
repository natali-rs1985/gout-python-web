################################################################################
#         Note book classes                                                    #
################################################################################
import re
import json
from collections import UserDict
import math
from addressbook import ViewerInterface


class Notebook(UserDict):

    def __init__(self, name, viewer):
        super().__init__()
        self.name = name
        self.current_page = 0
        self.records_on_the_page = 3
        self.viewer = viewer

    def add_note(self, note):
        self.data[note.id] = note

    def dump(self, file):  
        with open(file, 'w+') as write_file:
            dump_dict = {self.name:{}}
            for id in self.data.keys():
                dump_dict[self.name][str(id)] = {}
                dump_dict[self.name][str(id)]["keyword"] = [x for x in self.data[id].keyword]
                dump_dict[self.name][str(id)]["note"] = self.data[id].note
            json.dump(dump_dict, write_file)

    def load(self, file):   
        with open(file, 'r') as read_file:
            data = json.load(read_file)
            self.name = list(data.keys())[0]
            for id in list(data[self.name].keys()):
                note_ = Note(data[self.name][id]["note"])
                if "keyword" in data[self.name][id].keys():
                    for k in data[self.name][id]["keyword"]:
                        if k not in note_.keyword:
                            note_.keyword.append(k)
                self.add_note(note_)
            
    def delete(self, id):            
        if id in self.data.keys():
            self.data.pop(id)

    def __iter__(self):
        return self

    def __next__(self):
        print("Len of note book dictionary ", len(list(self.data.keys())))
        if self.current_page < int(math.ceil(len(list(self.data.keys()))/self.records_on_the_page)):
            keys = list(self.data.keys())
            r_list = []  
            for i in range(self.current_page * self.records_on_the_page, min([(self.current_page+1) * self.records_on_the_page, len(self.data)])):
                r_list.append(self.data[keys[i]])
            self.current_page += 1
            return r_list
        else:
            self.current_page = 0
        raise StopIteration

    def find(self, request_lst):
        if type(request_lst) == type(" "):
            request_lst = list(request_lst.split(" "))
        res_lst = []
        for teg in request_lst:
            teg = (
            teg.replace("+","\+")
               .replace("*", "\*")
               .replace("{", "\{")
               .replace("}", "\}")
               .replace("[", "\[")
               .replace("]", "\]")
               .replace("?", "\?")
               .replace("$", "\$")
               .replace("'\'", "\\")
               .lower() 
                  )
            for id in self.data:
                if re.search(teg," ".join(self.data[id].keyword).lower()) != None or re.search(teg, self.data[id].note.lower()) != None:
                    if self.data[id] not in res_lst:
                        res_lst.append(self.data[id])      
        return res_lst


class Note():
    id = 0

    def __init__(self, note):
        Note.id += 1
        self.id = Note.id
        self.keyword = []
        self.keyword = self.get_keywords(note)
        self.note = note

    def get_keywords(self, note):
        result_lst = []
        result = re.finditer("#[a-zA-Zа-яА-Я_\-\в]+", note)
        for group in result:
            result_lst.append(group.group(0)[1:])
        return result_lst

    def __str__(self):
        wide_str = len("___________________________________________________________")
        str_res = "      ID: "+str(self.id)+"\n"+"      Keywords:"
        kw_str = ""          
        str_count = 0
        for k in self.keyword:
            if str_count == wide_str:
                kw_str = kw_str+"\n"
                str_count = 0
            kw_str = kw_str+" #"+k
            str_count += len(" #"+k)
        str_res = str_res+kw_str
        str_res = str_res+"\n"
        str_count = 0    
        for i in range(len(self.note)):
            if str_count == wide_str:
                str_res = str_res+"\n"
                str_count = 0
            str_res = str_res+self.note[i]
            str_count += 1
        if str_res[-1] != "\n":
            str_res = str_res+"\n"
            
        return str_res+"-----------------------------------------------------------"
