from . import app
from .core import *
from flask import render_template, flash, request, redirect, url_for, g
import re


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/show_all')
def show_all():
    users = find_all()
    for user in users:
        if 'birthday' in user:
            user['birthday'] = str(user['birthday'].date())
    return render_template('show_all.html', users=users)


@app.route('/find_contact', methods=['GET', 'POST'])
def find_contact():
    if request.method == 'POST':
        name = request.form['name']
        if name in redis_list:
            res = find_in_redis(name)
            redis_list.remove(name)
            redis_list.insert(0, name)
            return render_template('find_contact.html', res=res)
        else:
            res = find_name(name)
            if not res:
                flash("Can't find record in the phone book")
                return redirect(url_for('find_contact'))
            else:
                if 'birthday' in res:
                    res['birthday'] = str(res['birthday'].date())
                verify_redis_list(name)

            return render_template('find_contact.html', res=res)

    else:
        return render_template('find_contact.html')


@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        rec = {}
        name = request.form['name']
        phone = request.form['phones']
        email = request.form['email']
        address = request.form['address']
        birthday = request.form['birthday']
        if find_name(name):
            flash("Contact with this name is already exist")
            return redirect(url_for('add_contact'))
        else:
            rec['name'] = name

        if phone:
            is_correct_format = re.search(r"\+?[\ \d\-\(\)]", phone)
            phone = sanitize_phone_number(phone)
            if not is_correct_format or len(phone) != 13:
                flash("Phone should have format: '[+] [XX] XXXXXXXXXX' (10 or 12 digits). Please try again")
                return render_template('add_contact.html')
            else:
                rec['phones'] = []
                rec['phones'].append(phone)

        if email:
            is_correct_format = re.search(r'[a-zA-Z0-9\.\-\_]+@[a-zA-Z0-9\-\_\.]+\.[a-z]{2,4}', email)
            if is_correct_format:
                rec['email'] = email
            else:
                flash("Email should have format: 'name@domain.[domains.]high_level_domain'. Try again.")
                return render_template('add_contact.html')

        if address:
            rec['address'] = address

        if birthday:
            is_correct_format = re.search(r'\d{2}.\d{2}.\d{4}', birthday)
            if is_correct_format:
                try:
                    birthday = datetime.strptime(birthday, '%d.%m.%Y')
                    rec['birthday'] = birthday
                except:
                    flash('Date has incorrect format, please try again')
                    return render_template('add_contact.html')
            else:
                flash('Date should have format "dd.mm.yyyy", please try again')
                return render_template('add_contact.html')

        contacts.insert_one(rec)
        if 'birthday' in rec:
            rec['birthday'] = str(rec['birthday'].date())
        return render_template('add_contact.html', rec=rec)

    else:
        return render_template('add_contact.html')


@app.route('/delete_contact', methods=['GET', 'POST'])
def delete_contact():
    if request.method == 'POST':
        name = request.form['name']
        res = find_name(name)
        if not res:
            flash("Can't find record in the phone book")
            return redirect(url_for('delete_contact'))
        else:
            contacts.delete_one({'name': name})

        return render_template('delete_contact.html', res=res)
    else:
        return render_template('delete_contact.html')


@app.route('/next_birthday', methods=['GET', 'POST'])
def next_birthday():
    if request.method == 'POST':
        days = request.form['days']
        days = int(days)
        res_lst = []
        for person in find_all():
            if days_to_birthday(person) < days:
                res_lst.append(person)

        if len(res_lst) == 0:
            flash("I'm sorry, couldn't find any")
            return redirect('next_birthday.html')
        else:
            for res in res_lst:
                res['birthday'] = str(res['birthday'].date())
            return render_template('next_birthday.html', res_lst=res_lst, days=days)

    else:
        return render_template('next_birthday.html')


name_ = ''


@app.route('/edit_contact', methods=['GET', 'POST'])
def edit_contact():
    global name_
    if request.method == 'POST':
        name = request.form['name']
        res = find_name(name)
        # if 'birthday' in res:
        #     res['birthday'] = str(res['birthday'].date())
        if not res:
            flash("Can't find record in the phone book")
            return redirect(url_for('edit_contact'))
        else:
            name_ = res['name']
            if name in redis_list:
                redis_list.remove(name)
            return render_template('edit_contact.html', res=res), name_
    else:
        return render_template('edit_contact.html')


@app.route('/edit_name', methods=['GET', 'POST'])
def edit_name():
    global name_
    if request.method == 'POST':
        name_new = request.form['name']
        if not find_name(name_new):
            contacts.update_one({'name': name_}, {"$set": {"name": name_new}})
            res = find_name(name_new)
            name_ = name_new
            if 'birthday' in res:
                res['birthday'] = str(res['birthday'].date())
            return render_template('edit_name.html', res=res), name_
        else:
            flash('Contact is already exist')
            return redirect(url_for('edit_name'))
    else:
        return render_template('edit_name.html')


@app.route('/edit_phone', methods=['GET', 'POST'])
def edit_phone():
    cont = find_name(name_)
    if request.method == 'GET':
        return render_template('edit_phones.html', cont=cont)
    else:
        phone = request.form['phone']
        is_correct_format = re.search(r"\+?[\ \d\-\(\)]", phone)
        phone = sanitize_phone_number(phone)
        if not is_correct_format or len(phone) != 13:
            flash("Phone should have format: '[+] [XX] XXXXXXXXXX' (10 or 12 digits). Please try again")
            return render_template('edit_phones.html', cont=cont)
        else:
            contacts.update_one({'name': name_}, {'$push': {'phones': phone}})
            cont = find_name(name_)
            return render_template('edit_phones.html', cont=cont)


@app.route('/edit_phone/<phone>', methods=['POST'])
def delete_phone(phone):
    contacts.update_one({'name': name_}, {'$pull': {'phones': phone}})
    flash('Phone was deleted')
    return redirect(url_for('edit_phone'))


@app.route('/edit_email', methods=['GET', 'POST'])
def edit_email():
    if request.method == 'POST':
        email = request.form['email']
        is_correct_format = re.search(r'[a-zA-Z0-9\.\-\_]+@[a-zA-Z0-9\-\_\.]+\.[a-z]{2,4}', email)
        if is_correct_format:
            contacts.update_one({'name': name_}, {'$set': {'email': email}})
            res = find_name(name_)
            if 'birthday' in res:
                res['birthday'] = str(res['birthday'].date())
            return render_template('edit_email.html', res=res)
        else:
            flash("Email should have format: 'name@domain.[domains.]high_level_domain'. Try again.")
            return render_template('edit_email.html')
    else:
        return render_template('edit_email.html')


@app.route('/edit_address', methods=['GET', 'POST'])
def edit_address():
    if request.method == 'POST':
        address = request.form['address']
        contacts.update_one({'name': name_}, {'$set': {'address': address}})
        res = find_name(name_)
        if 'birthday' in res:
            res['birthday'] = str(res['birthday'].date())
        return render_template('edit_address.html', res=res)
    else:
        return render_template('edit_address.html')


@app.route('/edit_birthday', methods=['GET', 'POST'])
def edit_birthday():
    if request.method == 'POST':
        birthday = request.form['birthday']
        is_correct_format = re.search(r'\d{2}.\d{2}.\d{4}', birthday)
        if is_correct_format:
            try:
                birthday = datetime.strptime(birthday, '%d.%m.%Y')
                contacts.update_one({'name': name_}, {'$set': {'birthday': birthday}})
                res = find_name(name_)
                res['birthday'] = str(res['birthday'].date())
                return render_template('edit_birthday.html', res=res)
            except:
                flash('Date has incorrect format, please try again')
                return render_template('edit_birthday.html')
        else:
            flash('Date should have format "dd.mm.yyyy", please try again')
            return render_template('edit_birthday.html')

    else:
        return render_template('edit_birthday.html')
