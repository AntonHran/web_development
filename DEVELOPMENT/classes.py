from collections import UserDict
import re
from abc import ABC, abstractmethod
import datetime
from typing import Any, List
from exceptions_address_book import *

UKR_MOBILE_PHONE_CODES = ['095', '099', '050', '063', '066', '067', '077', '0800', '045', '046', '032',
                          '044', '048', '068', '097', '098', '091', '092', '094', ]


class TerminalPrint(ABC):
    @abstractmethod
    def display(self, text: str) -> None:
        raise NotImplementedError


class Field(ABC):
    @abstractmethod
    def get_value(self):
        raise NotImplementedError

    @abstractmethod
    def set_value(self, value):
        raise NotImplementedError

    @abstractmethod
    def _check_value(self, value):
        raise NotImplementedError

    @abstractmethod
    def display(self, output: TerminalPrint) -> None:
        raise NotImplementedError


class UnnecessaryField(ABC):
    @abstractmethod
    def get_value(self):
        raise NotImplementedError

    @abstractmethod
    def set_value(self, value):
        raise NotImplementedError

    @abstractmethod
    def display(self, output: TerminalPrint) -> None:
        raise NotImplementedError


class Output(TerminalPrint):
    def display(self, text: str) -> None:
        print(text)


class View(ABC):
    @abstractmethod
    def add_command(self, command):
        pass

    @abstractmethod
    def display_commands(self):
        pass


class TerminalView(View):
    def __init__(self):
        self.commands = []

    def add_command(self, command: str) -> None:
        self.commands.append(command)

    def display_commands(self) -> list:
        return self.commands


class Name(Field):
    def __init__(self, name: str):
        _name = self._check_value(name)
        if _name:
            self.__name = _name

    def get_value(self) -> str:
        return self.__name

    def set_value(self, newname: str) -> None:
        _value = self._check_value(newname)
        if _value:
            self.__name = _value

    def _check_value(self, name: str) -> str | Exception:
        if name and isinstance(name, str) and len(name) > 1:
            return name
        else:
            raise NameNotFilledException

    def display(self, output: TerminalPrint) -> None:
        output.display(f'Name: {self.__name}')


class Phone(Field):
    def __init__(self, phone_number: str) -> None:
        self.__phone_number = []
        _value = self._check_value(phone_number)
        if _value:
            self.__phone_number.append(_value)

    def get_value(self) -> list[str]:
        return self.__phone_number

    def _check_value(self, phone_num: str) -> str | None:
        if phone_num:
            phone_num = re.sub(r'[+\-() ]', '', phone_num)
            if re.fullmatch(r'^([0-9]){6,14}[0-9]$', phone_num):
                for inner_code in UKR_MOBILE_PHONE_CODES:
                    if phone_num.startswith(inner_code):
                        return f'+38{phone_num}'
            else:
                raise ValidPhoneException(phone_num)
        return None

    def set_value(self, phone_number: str) -> None:
        _number = self._check_value(phone_number)
        if _number and _number not in self.__phone_number:
            self.__phone_number.append(_number)
        elif not _number:
            raise PhoneNumberNotFilledException
        else:
            raise PhoneExistException(_number)

    def delete_phone_number(self, phone_number: str) -> None:
        number_find = [num for num in self.__phone_number if re.search(phone_number, num)]
        if number_find:
            self.__phone_number.remove(*number_find)
        raise PhoneNotExistException(phone_number)

    def display(self, output: TerminalPrint) -> None:
        output.display(f'Phone number(-s): {self.__phone_number}')


class Email(Field):
    def __init__(self, email: str = None) -> None:
        _value = self._check_value(email)
        self.__email = _value

    def get_value(self) -> str:
        return self.__email

    def set_value(self, new_email: str) -> None:
        self.__email = self._check_value(new_email)

    def _check_value(self, email: str) -> str | None:
        if email and re.match(r"([a-zA-Z.]+\w+\.?)+(@\w{2,}\.)(\w{2,})", email):
            return email
        elif not email:
            return None
        else:
            raise ValidEmailException(email)

    def display(self, output: TerminalPrint) -> None:
        output.display(f'Email: {self.__email}')


class BirthDay(Field):
    def __init__(self, birth_date: str = None):
        _value = self._check_value(birth_date)
        self.__birth_date = _value

    def get_value(self) -> datetime.date:
        return self.__birth_date

    def set_value(self, birth_date_: str) -> None:
        self.__birth_date = self._check_value(birth_date_)

    def _check_value(self, birthday: str) -> datetime.date | None | Exception:
        if birthday:
            try:
                year, month, day = birthday.strip().split('-')
            except ValueError:
                raise ValidBirthDateException(birthday)
            try:
                return datetime.date(int(year), int(month), int(day))
            except ValueError:
                raise ValidBirthDateFormatException(birthday)
        else:
            return None

    def days_to_birthday(self) -> int:
        if self.__birth_date:
            current_date: datetime.date = datetime.date.today()
            birthday: datetime.date = datetime.date(year=current_date.year, month=self.__birth_date.month,
                                                    day=self.__birth_date.day)
            diff: int = (birthday - current_date).days
            if diff < 0:
                birthday: datetime.date = datetime.date(year=current_date.year + 1, month=self.__birth_date.month,
                                                        day=self.__birth_date.day)
                diff = (birthday - current_date).days
            return diff
        raise BirthdayNotExistException

    def display(self, output: TerminalPrint) -> None:
        output.display(f'Birthday: {self.__birth_date.strftime("%A %d %B %Y") if self.__birth_date else None}')


class Status(Field):
    def __init__(self, status: str = None):
        self.statuses = ['Friend', 'Family', 'Co-Worker', 'Special', None]
        _status = self._check_value(status)
        self.__status = _status

    def get_value(self) -> str:
        return self.__status

    def set_value(self, new_status: str) -> None:
        self.__status = self._check_value(new_status)

    def _check_value(self, status: str) -> str:
        if status in self.statuses:
            return status
        raise StatusNotExistException(status)

    def display(self, output: TerminalPrint) -> None:
        output.display(f'Status: {self.__status}')


class Note(UnnecessaryField):
    def __init__(self, note: str = None):
        self._note = note

    def get_value(self) -> str:
        return self._note

    def set_value(self, new_note: str) -> None:
        self._note = new_note

    def display(self, output: TerminalPrint) -> None:
        output.display(f'Note: {self._note}')


class Record:
    def __init__(self, name: Field, phone: Field = None, email: Field = None,
                 bd: Field = None, status: Field = None, note: UnnecessaryField = None) -> None:
        self.name = name
        self.phone = Phone('') if not phone else phone
        self.email = Email() if not email else email
        self.bd = BirthDay() if not bd else bd
        self.status = Status() if not status else status
        self.note = Note() if not note else note

    def _get_fields(self) -> dict:
        fields_dict: dict = {name: value.get_value() for (name, value) in vars(self).items()}
        return fields_dict

    @staticmethod
    def _parser(element: Any) -> str:
        if isinstance(element, list):
            return ' '.join(element)
        elif isinstance(element, datetime.date):
            return element.strftime('%A %d %B %Y')
        elif isinstance(element, str):
            return element

    def search(self, parameter: str) -> str:
        data = self._get_fields()
        for value in data.values():
            if value and re.search(parameter, self._parser(value), flags=re.I):
                return value

    def display(self, output: TerminalPrint) -> None:
        for field in vars(self).values():
            field.display(output)

    def display_field(self, field_name: str, output: TerminalPrint) -> None | Exception:
        return vars(self)[field_name].display(output) if field_name in vars(self).keys() else FieldNotExistException


class AddressBook(UserDict):

    def add_record(self, record: Record) -> None:
        if record.name.get_value() in self.data:
            raise RecordExistException(record.name.get_value())
        self.data[record.name.get_value()] = record

    def delete_record(self, name: str) -> None:
        name = self.search_by_name(name)
        if name not in self.data:
            raise RecordNotExistException(name)
        del self.data[name]

    def iterator(self, page: int) -> list:
        start: int = 0
        while True:
            data = list(self.data.values())[start: start+page]
            if not data:
                break
            yield data
            start += page

    def search_by_keyword(self, parameter: str) -> List[Record] | str:
        res = []
        for record in self.data.values():
            if record.search(parameter):
                res.append(record)
        return res if res else SearchException(parameter)

    def search_by_name(self, name) -> str:
        for key in self.data:
            if re.search(name, key, flags=re.I):
                return key
        raise NameNotExistException(name)


contacts = AddressBook()
output_ = Output()
commands_addressbook = TerminalView()
