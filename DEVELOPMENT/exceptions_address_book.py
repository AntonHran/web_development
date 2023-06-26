class NameNotFilledException(Exception):
    def __init__(self, message='Name can not be missing/empty.') -> None:
        self.message = message
        super().__init__(self.message)


class PhoneNumberNotFilledException(Exception):
    def __init__(self, message='You can not add empty value as a phone number!!!') -> None:
        self.message = message
        super().__init__(self.message)


class ValidPhoneException(Exception):
    def __init__(self, number_for_validation: str) -> None:
        self.message = f'Wrong format - {number_for_validation} - of a phone number.'
        super().__init__(self.message)


class ValidEmailException(Exception):
    def __init__(self, email_for_validation: str) -> None:
        self.message = f'Wrong format - {email_for_validation} - of an email.'
        super().__init__(self.message)


class ValidBirthDateException(Exception):
    def __init__(self, birth_date_for_validation: str) -> None:
        self.message = f'Wrong format - {birth_date_for_validation} - of a birthdate.'
        super().__init__(self.message)


class ValidBirthDateFormatException(Exception):
    def __init__(self, birth_date_for_verification: str) -> None:
        self.message = f'Birth date {birth_date_for_verification} does not valid.'
        super().__init__(self.message)


class PhoneExistException(Exception):
    def __init__(self, number_for_verification: str) -> None:
        self.message = f'Number {number_for_verification} already exists.'
        super().__init__(self.message)


class SearchException(Exception):
    def __init__(self, arg_for_search: str) -> None:
        self.message = f'There are not matches with {arg_for_search}...'
        super().__init__(self.message)


class NameNotExistException(Exception):
    def __init__(self, name_for_verification: str) -> None:
        self.message = f'Name {name_for_verification} does not exist.'
        super().__init__(self.message)


class PhoneNotExistException(Exception):
    def __init__(self, number_for_verification: str) -> None:
        self.message = f'Number {number_for_verification} does not exist.'
        super().__init__(self.message)


class BirthdayNotExistException(Exception):
    def __init__(self, message: str = 'Birthday does not exist for this contact.') -> None:
        self.message = message
        super().__init__(self.message)


class StatusNotExistException(Exception):
    def __init__(self, status_for_verification: str) -> None:
        self.message = f'Status {status_for_verification} does not exist.'
        super().__init__(self.message)


class RecordExistException(Exception):
    def __init__(self, record_for_verification: str) -> None:
        self.message = f'Record with a such name {record_for_verification} already exists.'
        super().__init__(self.message)


class RecordNotExistException(Exception):
    def __init__(self, record_for_verification: str) -> None:
        self.message = f'Record with a such name {record_for_verification} does not exist.'
        super().__init__(self.message)


class FieldNotExistException(Exception):
    def __init__(self, field_for_verification: str) -> None:
        self.message = f'A such field: {field_for_verification} does not exist.'
        super().__init__(self.message)
