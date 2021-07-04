from abc import abstractmethod, ABC
import pickle
import json


class SerializationInterface(ABC):

    @abstractmethod
    def serialize(self, data):
        pass

    @abstractmethod
    def deserialize(self):
        pass


class SerializatoinListBin(SerializationInterface):

    def __init__(self):
        self.file = 'list.bin'

    def serialize(self, data):
        with open(self.file, 'wb') as fh:
            pickle.dump(data, fh)

    def deserialize(self):
        with open(self.file, 'rb') as fh:
            my_list = pickle.load(fh)
        return my_list


class SerializatoinDictBin(SerializationInterface):

    def __init__(self):
        self.file = 'dict.bin'

    def serialize(self, data):
        with open(self.file, 'wb') as fh:
            pickle.dump(data, fh)

    def deserialize(self):
        with open(self.file, 'rb') as fh:
            my_dict = pickle.load(fh)
        return my_dict


class SerializatoinTupleBin(SerializationInterface):

    def __init__(self):
        self.file = 'tuple.bin'

    def serialize(self, data):
        with open(self.file, 'wb') as fh:
            pickle.dump(data, fh)

    def deserialize(self):
        with open(self.file, 'rb') as fh:
            my_tuple = pickle.load(fh)
        return my_tuple


class SerializatoinSetBin(SerializationInterface):

    def __init__(self):
        self.file = 'set.bin'

    def serialize(self, data):
        with open(self.file, 'wb') as fh:
            pickle.dump(data, fh)

    def deserialize(self):
        with open(self.file, 'rb') as fh:
            my_set = pickle.load(fh)
        return my_set


class SerializatoinListJson(SerializationInterface):

    def __init__(self):
        self.file = 'list.json'

    def serialize(self, data):
        with open(self.file, 'w') as fh:
            json.dump(data, fh)

    def deserialize(self):
        with open(self.file, 'r') as fh:
            my_list = json.load(fh)
        return my_list


class SerializatoinDictJson(SerializationInterface):

    def __init__(self):
        self.file = 'dict.json'

    def serialize(self, data):
        with open(self.file, 'w') as fh:
            json.dump(data, fh)

    def deserialize(self):
        with open(self.file, 'r') as fh:
            my_dict = json.load(fh)
        return my_dict


class SerializatoinTupleJson(SerializationInterface):

    def __init__(self):
        self.file = 'tuple.json'

    def serialize(self, data):
        with open(self.file, 'w') as fh:
            json.dump(data, fh)

    def deserialize(self):
        with open(self.file, 'r') as fh:
            my_tuple = json.load(fh)
        return tuple(my_tuple)


class SerializatoinSetJson(SerializationInterface):

    def __init__(self):
        self.file = 'set.json'

    def serialize(self, data):
        data = list(data)
        with open(self.file, 'w') as fh:
            json.dump(data, fh)

    def deserialize(self):
        with open(self.file, 'r') as fh:
            my_set = json.load(fh)
        return set(my_set)


if __name__ == '__main__':
    ser_list = ['my', 1, 4, 'new']
    ser_dict = {'me': 1, 'ты': 2}
    ser_tuple = ('hgf', 'рпрп', 1)
    ser_set = {'hgsa', 'qwe', 'я люблю жизнь', 4}

    serlist = SerializatoinListBin()
    serlist.serialize(ser_list)
    print(serlist.deserialize())

    serdict = SerializatoinDictBin()
    serdict.serialize(ser_dict)
    print(serdict.deserialize())

    sertuple = SerializatoinTupleBin()
    sertuple.serialize(ser_tuple)
    print(sertuple.deserialize())

    serset = SerializatoinSetBin()
    serset.serialize(ser_set)
    print(serset.deserialize())

    serlistjson = SerializatoinListJson()
    serlistjson.serialize(ser_list)
    print(serlistjson.deserialize())

    serdictjson = SerializatoinDictJson()
    serdictjson.serialize(ser_dict)
    print(serdictjson.deserialize())

    sertuplejson = SerializatoinTupleJson()
    sertuplejson.serialize(ser_tuple)
    print(sertuplejson.deserialize())

    sersetjson = SerializatoinSetJson()
    sersetjson.serialize(ser_set)
    print(sersetjson.deserialize())