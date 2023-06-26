import re
from classes import AddressBook, Record, Name, contacts, output_, commands_addressbook, TerminalView, TerminalPrint
import pickle
from functools import wraps
import collections


def input_error(func):
    @wraps(func)
    def inner_func(*args):
        try:
            return func(*args) if args else func()
        except Exception as exc:
            print(exc)
        except (KeyError, ValueError, IndexError, TypeError) as error:
            print(f'''Error: {error}. Please check the accordance of the entered data to the requirements.
And also a correctness of the entered name or/and phone number. And, of course, their existence.''')
    return inner_func


def write_info_from_class(obj: AddressBook) -> None:
    with open('contacts.bin', 'wb') as fr:
        pickle.dump(obj, fr)


def read_info_from_file() -> AddressBook:
    with open('contacts.bin', 'rb') as fr:
        contacts_from_file: AddressBook = pickle.load(fr)
    return contacts_from_file


@input_error
def add_contact(name: str, contact_book: AddressBook) -> None:
    name: Name = Name(name)
    record: Record = Record(name)
    contact_book.add_record(record)
    write_info_from_class(contact_book)


add_contact_comm = """
    A name of a contact.
    The field name cannot be empty.
    To create a new contact, type: add contact <name of a new contact>"""
commands_addressbook.add_command(add_contact_comm)


@input_error
def delete_contact(name: str, contact: AddressBook) -> None:
    contact.delete_record(name)
    write_info_from_class(contact)


delete_contact_comm = """
    To delete some contact, type: delete contact <name of a contact>"""
commands_addressbook.add_command(delete_contact_comm)


@input_error
def search(keyword: str, contact: AddressBook, output: TerminalPrint) -> None:
    result: list = contact.search_by_keyword(keyword)
    [res.display(output) for res in result]


search_comm = """
    To search a contact by a name or a phone or an email a date of birth or a status or other fields,
    using a full value of the field name or only a part of it, type: search <keyword>"""
commands_addressbook.add_command(search_comm)


def show_contacts(output: TerminalPrint, pages: int = 2) -> None:
    contacts_download = read_info_from_file()
    for record in contacts_download.iterator(pages):
        [field.display(output) for field in record]
        input('Press "Enter": ')


show_contacts_comm = """
    To show all notices of an address book, type: show all"""
commands_addressbook.add_command(show_contacts_comm)


def show_commands(commands: TerminalView) -> None:
    print('\n\tGeneral commands for all written contacts:\n'
          '\tNames, phone numbers, emails and other parameters have to be written without brackets <...>')
    for command in commands.display_commands():
        print(command)


show_commands_comm = """
    To show a list of all commands with instructions, type: help"""
commands_addressbook.add_command(show_commands_comm)


@input_error
def change_name(name: str, contact: AddressBook) -> None:
    name: str = contact.search_by_name(name)
    contact_data: Record = contact.data[name]
    contact.delete_record(name)
    new_name: str = input('Please enter a new name for the contact: ')
    contact_data.name.set_value(new_name)
    contact.add_record(contact_data)
    write_info_from_class(contact)


change_name_comm = """
    To change the name of some contact, type: change name <name of contact>"""
commands_addressbook.add_command(change_name_comm)


@input_error
def add_phone_number(name: str, contact: AddressBook) -> None:
    name = contact.search_by_name(name)
    number: str = input('Please enter a phone number according to a phone pattern: +<code of a country>XXXXXXXXX '
                        'or <operator code>XXXXXXX: ')
    contact.data[name].phone.set_value(number)
    write_info_from_class(contact)


add_phone_number_comm = """
    A phone number of a contact.
    All phone numbers should be added according to a phone pattern: +<code of a country>XXXXXXXXX or
    <operator code>XXXXXXX
    All phone numbers are saved according to the pattern: +<code of a country>(XX)XXXXXXX

    To add a new phone number to some contact, type: add phone <name of a contact>"""
commands_addressbook.add_command(add_phone_number_comm)


@input_error
def delete_phone_number(name: str, contact: AddressBook) -> None:
    name = contact.search_by_name(name)
    number: str = input('Please enter a number to delete: ')
    contact.data[name].phone.delete_phone_number(number)
    write_info_from_class(contact)


delete_phone_number_comm = """
    To change a phone number of some contact, type: change phone <name of a contact>"""
commands_addressbook.add_command(delete_phone_number_comm)


@input_error
def change_phone_number(name: str, contact: AddressBook) -> None:
    name = contact.search_by_name(name)
    phone_num: str = input('Enter <an old phone number>-<new phone number> for the contact: ')
    old, new = phone_num.strip().split('-')
    contact.data[name].phone.delete_phone_number(old)
    contact.data[name].phone.set_value(new)
    write_info_from_class(contact)


change_phone_number_comm = """
    To change a phone number of some contact, type: change phone <name of a contact>"""
commands_addressbook.add_command(change_phone_number_comm)


@input_error
def change_email(name: str, contact: AddressBook) -> None:
    name = contact.search_by_name(name)
    email: str = input('Please enter an email for the contact: ')
    contact.data[name].email.set_value(email)
    write_info_from_class(contact)


change_email_comm = """
    An email of a contact.
    All emails should be written according to a valid format of your email type.
    To change or add (if this field is empty), an email of some contact, type: change email <name of a contact>"""
commands_addressbook.add_command(change_email_comm)


@input_error
def change_birthdate(name: str, contact: AddressBook) -> None:
    name = contact.search_by_name(name)
    birthdate: str = input('Please enter a date of birth for the contact according to pattern YYYY-MM-DD: ')
    contact.data[name].bd.set_value(birthdate)
    write_info_from_class(contact)


change_birthdate_comm = """
    A birthday of a contact.
    All dates of the birthday should be written according to the pattern: YYYY-MM-DD
    To change/add (if this field is empty) a birthdate of some contact, type:
    change bd <name of a contact>"""
commands_addressbook.add_command(change_birthdate_comm)


@input_error
def days_to_birthday(name: str, contact: AddressBook) -> None:
    name = contact.search_by_name(name)
    print(f'Number days to birthday for {name} is {contact.data[name].bd.days_to_birthday()} days.')


days_to_birthday_comm = """
    To show how many days left to someone's birthday, type: days to bd <name of a contact>"""
commands_addressbook.add_command(days_to_birthday_comm)


@input_error
def change_status(name: str, contact: AddressBook) -> None:
    name = contact.search_by_name(name)
    status: str = input('Please enter one of statuses to this contact: '
                        'Friend, Family, Co-Worker, Special. Or leave it empty: ')
    contact.data[name].status.set_value(status)
    write_info_from_class(contact)


change_status_comm = """
    A status of a contact.
    You can add one of the following statuses to your contact: Friend, Family, Co-Worker, Special.
    Or it can be empty.
    To add/change a status of some contact, type: change status <name of a contact>"""
commands_addressbook.add_command(change_status_comm)


@input_error
def add_note(name: str, contact: AddressBook) -> None:
    name = contact.search_by_name(name)
    note: str = input('Please enter a note for the contact: ')
    contact.data[name].note.set_value(note)
    write_info_from_class(contact)


add_note_comm = """
    A note of a contact.
    To add/change notes of some contact, type: change note <name of a contact>
    Or it can be empty."""
commands_addressbook.add_command(add_note_comm)


@input_error
def show_field(name: str, contact: AddressBook, output: TerminalView) -> None:
    name_check = contact.search_by_name(name)
    field: str = input('Please type a field you want to see for this contact: ')
    contact.data[name_check].display_field(field, output)


show_field_comm = """
    To show the necessary field of some contact, type: show field <name of a contact>"""
commands_addressbook.add_command(show_field_comm)


def farewell(contact: AddressBook) -> None:
    write_info_from_class(contact)
    print('All changes saved successfully.\n'
          '\nYou returned to the main Menu.')


farewell_comm = """
    To exit the addressbook and come back to the main menu, type: back"""
commands_addressbook.add_command(farewell_comm)


def greeting(contact: AddressBook):
    print('\n\tNow you are in your personal addressbook.\n'
          '\tI can help you with adding, changing, showing and storing all contacts and data connected with them.')
    try:
        contact.data.clear()
        [contact.add_record(value) for value in read_info_from_file().values()]
    except (FileExistsError, FileNotFoundError):
        print('There are not records yet. Your addressbook is empty.')


# ----------------------------------------------------------------------------------------------------------------------
Function = collections.namedtuple('Function', ['function', 'records', 'terminal_output', 'terminal_commands'])

methods = {'add contact': Function(add_contact, AddressBook, '', ''),
           'delete contact': Function(delete_contact, AddressBook, '', ''),
           'search': Function(search, AddressBook, TerminalPrint, ''),
           'show all': Function(show_contacts, '', TerminalPrint, ''),
           'change name': Function(change_name, AddressBook, '', ''),
           'add phone': Function(add_phone_number, AddressBook, '', ''),
           'change phone': Function(change_phone_number, AddressBook, '', ''),
           'delete phone': Function(delete_phone_number, AddressBook, '', ''),
           'change email': Function(change_email, AddressBook, '', ''),
           'change bd': Function(change_birthdate, AddressBook, '', ''),
           'days to bd': Function(days_to_birthday, AddressBook, '', ''),
           'change status': Function(change_status, AddressBook, '', ''),
           'add note': Function(add_note, AddressBook, '', ''),
           'help': Function(show_commands, '', '', TerminalView),
           'show field': Function(show_field, AddressBook, TerminalPrint, ''), }


@input_error
def command_parser(command: str) -> tuple:
    for func in methods:
        if re.search(func, command, flags=re.I):
            return func, re.sub(func, '', command, flags=re.I).strip()


def handler(function_name: str) -> collections.namedtuple:  # Tuple[Callable, None | AddressBook, None | TerminalView]:
    return methods[function_name]


def make_function(text: str) -> None:
    try:
        command, argument = command_parser(text)
        func: collections.namedtuple = handler(command)
        if argument and func.records and func.terminal_output:
            func.function(argument, contacts, output_)
        elif argument and func.records and not func.terminal_output:
            func.function(argument, contacts)
        elif argument and func.terminal_output and not func.records:
            func.function(argument, output_)
        elif not argument and func.terminal_output and not func.records:
            func.function(output_)
        elif not argument and func.terminal_commands and not func.records:
            func.function(commands_addressbook)

    except (TypeError, KeyError):
        print('I do not understand what you want to do. Please look at the commands.')


def address_book_main():
    greeting(contacts)
    show_commands(commands_addressbook)
    while True:
        text: str = input('\nEnter your command: ')
        if text == 'back':
            farewell(contacts)
            break
        make_function(text)
