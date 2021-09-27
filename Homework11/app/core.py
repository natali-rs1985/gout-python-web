import warnings
from datetime import datetime
import redis
import pymongo
from pymongo.database import Database
from pymongo.collection import Collection


redis = redis.Redis(host='localhost', port=6379, db=5)

cont_uri = "mongodb://admin:123qwe@localhost:27017/assistant?retryWrites=true&w=majority"
client = pymongo.MongoClient(cont_uri)
assistant: Database = client.assistant
contacts: Collection = assistant.contacts

warnings.filterwarnings('ignore')


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


def find_name(name):
    name = contacts.find_one({'name': name})
    return name


def find_all():
    users = list(contacts.find())
    return users


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
