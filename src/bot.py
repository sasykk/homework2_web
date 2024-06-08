import pickle
import typing
from typing import List
from .clean_folder import Cleaner
from .classes import *
from .exceptions import *
from .notes import *
from abc import ABC, abstractmethod
# from .clean_folder import Cleaner
# from .classes import *
# from .exceptions import *
# from .notes import *

TEXT = \
    """
    1. Add contact with additional info:      - - - > add info name phone birthday email address (example: add info denis 1234567890 20.12.2012 goit@mail.com Kiev)
    2. Add phone                              - - - > add phone name phone_number (example: add phone denis 1234567890)
    3. Add address                            - - - > add address name address (example: add address denis Kiev)
    4. Add note                               - - - > add note title text (example: add note shopping_list "Buy milk, eggs, and bread")
    5. Add birthday                           - - - > add birthday name (example: add birthday denis 12.12.2012)
    6. Add email                              - - - > add email name email_address (example: add email denis goit@mail.com)
    7. Add contact                            - - - > add name (example: add denis)
    8. Edit note                              - - - > edit note old_title new_text (example: edit note shopping_list grocery_list "Buy milk, eggs, and bread")
    9. Edit name                              - - - > edit name old_name new_name (example: edit name denis andrew)
    10. Edit phone                            - - - > edit phone name old_phone new_phone (example: edit phone andrew 1234567890 01234789)
    11. Edit birthday                         - - - > edit birthday name new_birthday (example: edit birthday kolya 12.12.2000)
    12. Edit email                            - - - > edit email name old_email new_email (example: edit email kolya old_email new_email)
    13. Remove                                - - - > remove name (example: remove denis)
    14. Remove note                           - - - > remove note title (example: remove note shopping_list)
    15. Remove address                        - - - > remove address name address (example: remove address denis)
    16. Contacts birthday                     - - - > contacts birthday days (example: contacts birthday 5)
    17. Show all notes                        - - - > show all notes
    18. Show all                              - - - > show all
    19. Search note                           - - - > search note text (example: search note milk)
    20. Search                                - - - > search text (example: search denis)
    21. Days to birthdays                     - - - > days to birthdays name (example: days to birthdays denis)
    22. Folder cleaner.                       - - - > clean <path> - simple file sorter
    23. Help                                  - - - > help
    24. Exit                                  - - - > exit
    """

class UserInterface(ABC):
    @abstractmethod
    def display(self, message):
        pass

    @abstractmethod
    def get_input(self):
        pass

class ConsoleInterface(UserInterface):
    def display(self, message):
        print(message)

    def get_input(self):
        return input('> ')

class Bot:
    
    def __init__(self, user_interface=None):
        self.file = 'phone_book.pickle'
        self.book = AddressBook()
        self.raw_path = ""
        try:
            with open(self.file, 'rb') as fh:
                read_book = pickle.load(fh)
                self.book.data = read_book
        except FileNotFoundError:
            print('New phone book has been created\n')
        self.file_note = 'note_book.pickle'
        self.notes = Note()
        try:
            with open(self.file_note, 'rb') as fh:
                read_note = pickle.load(fh)
                self.notes.data = read_note
        except FileNotFoundError:
            print('New book of notes has been created\n')
        self.ui = user_interface or ConsoleInterface()

    def input_error(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyError:
                return ('\n  There is no contact with this name!\n')
            except ValueError:
                return ('\n  Check the phone number! Should be 10 digits\n')
            except IndexError:
                return ('\n  Check your input!\n')
            except FileNotFoundError:
                return ('\n  Path is not exist!\n')
            except AddressIsExist:
                return ('\n  Address is exist!\n')
            except AddressIsNotExist:
                return ('\n  Address is not exist!\n')
            except AttributeError:
                return ('\n  Check your input!\n')
        return inner

    @input_error
    def add_contact_phone_birthday_email_address(self, book, data: List[list]):
        data = data[0]
        name = data[0]
        phone = data[1]
        birthday = None
        address = None
        email = None
        if len(data) > 2:
            birthday = data[2]
        if len(data) > 3:
            email = data[3]
        if len(data) > 4:
            address = " ".join(data[4:])
        record = Record(name, phone, birthday, address, email)
        result = book.add_record(record)
        if result:
            print('\n Record has been added')
        return record

    @input_error
    def add_contact(self, book, data):
        record = Record(Name(data[0][0]))
        result = book.add_record(record)
        if result:
            print('\n Contact has been added \n')
        return record

    @input_error
    def add_phone(self, book, data):
        data = data[0]
        name = data[0]
        record = book.find(name)
        phone = data[1]
        result = record.add_phone(phone)
        if result:
            print('\n Phone has been added\n')
        return record

    @input_error
    def add_birthday(self, book, data):
        data = data[0]
        name = data[0]
        record = book.find(name)
        birthday = data[1]
        result = record.add_birthday(birthday)
        if result:
            print('\n Birthday has been added\n')
        return record

    @input_error
    def add_address(self, book, data):
        data = data[0]
        name = data[0]
        address = " ".join(data[1:])
        record = book.find(name)
        record.add_address(address)
        print('\n Address has been added\n')
        return record

    @input_error
    def add_email(self, book, data):
        data = data[0]
        name = data[0]
        record = book.find(name)
        mail = data[1]
        result = record.add_email(mail)
        if result:
            print('\n Email has been added\n')

    @input_error
    def remove_address(self, book, data):
        data = data[0]
        name = data[0]
        address = " ".join(data[1:])
        record = book.find(name)
        record.remove_address(address)
        print('\n Address has been removed')
        return record

    def console_input(self):
        usr_input = input('> ')
        self.raw_path = usr_input
        return usr_input.lower().strip()

    @input_error
    def edit_name(self, book, data):
        data = data[0]
        old_name, new_name = data
        record = book.edit_record(old_name, new_name)
        return record

    @input_error
    def edit_phone(self, book, data):
        data = data[0]
        name, old_phone, new_phone = data
        record = book.find(name)
        record.edit_phone(old_phone, new_phone)
        return record

    @input_error
    def edit_birthday(self, book, data):
        data = data[0]
        name, birthday = data
        record = book.find(name)
        record.add_birthday(birthday)
        return record

    @input_error
    def edit_email(self, book, data):
        data = data[0]
        name, old_email, new_email = data
        record = book.find(name)
        record.edit_email(old_email, new_email)
        return record

    @input_error
    def days_to_birthday(self, book, data):
        name = data[0][0]
        record = book.find(name)
        if record:
            result = record.days_to_birthday()
            return f"Days to birthday: {result}"

    @input_error
    def contacts_birthday(self, book, data):
        data = data[0]
        days = int(data[0])
        result = []
        for record in book.values():
            if record.birthday:
                if record.days_to_birthday() < days:
                    result.append(record)
        if result != []:
            return result
        else:
            return 'There are no contacts for congratulations'

    @input_error
    def find(self, book, data):
        search = data[0]
        if search.isdigit():
            phone = search
            for name, record in book.items():
                if record.find_phone(phone):
                    return f'\n{record}\n'
                else:
                    raise KeyError
        else:
            result = book.find(search)
            if not result:
                raise KeyError
            return result

    @input_error
    def clean(self, data=None, path=None):
        cleaner = Cleaner(self.raw_path.strip().split()[1])
        cleaner.clean()

    def hello(self, book, data):
        return '\n  Hello how can I help you?\n'

    def help(self, *_):
        return TEXT

    @input_error
    def good_bye(self, book, data):
        try:
            with open('phone_book.pickle', 'wb') as fh:
                pickle.dump(book.data, fh)
        except Exception as e:
            return (e)
        try:
            with open('note_book.pickle', 'wb') as fh:
                pickle.dump(self.notes.data, fh)
        except Exception as e:
            return (e)
        return 'Good bye!'

    @input_error
    def remove(self, book, data):
        data = data[0]
        name = data[0]
        if len(data) == 1:
            record = book.delete(name)
            return '\n  Contact has been removed\n'
        else:
            phone = data[1]
            record = book.find(name)
            book.delete(record)
            if record:
                record.remove_phone(phone)
                return record
            else:
                raise KeyError

    @input_error
    def search(self, book, data):
        text = data[0][0]
        result = book.search(text)
        if result != []:
            for record in result:
                print(record)
        else:
            print('\n  No results \n')

    def show_all(self, book, data):
        if not book:
            print('\n Phone book is empty\n')
        else:
            for record in book.iterator(5):
                print(*record, sep='\n')

    def add_note(self, book, data):
        data = data[0]
        note_title = data[0]
        note_text = ' '.join(data[1:])
        notes = self.notes
        result = notes.add(note_title, note_text)
        return result

    def edit_note(self, book, data):
        data = data[0]
        note_title = data[0]
        new_text = ' '.join(data[1:])
        notes = self.notes
        result = notes.edit(note_title, new_text)
        if result == False:
            return 'Note not found'
        return result

    def remove_note(self, book, data):
        data = data[0]
        note_title = data[0]
        notes = self.notes
        result = notes.delete(note_title)
        if result == False:
            return 'Note not found'
        return 'Note has been removed'

    def search_note(self, book, data):
        data = data[0]
        request = data[0]
        notes = self.notes
        result = notes.search(request)
        for note in result:
            title = note[0]
            text = note[1]
            print(f'  {title.title()}: {text}')
        return

    def show_all_notes(self, book, data):
        result = self.notes.print_all_notes()
        print(result)

    @input_error
    def parser(self, user_input, commands):
        for command in commands:
            if user_input.startswith(command):
                data = user_input.replace(command, '').split()
                # data = user_input.split()[1:]
                return commands[command], data
        else:
            raise IndexError

    def run(self):

        commands = {
            "add info": self.add_contact_phone_birthday_email_address,
            "add phone": self.add_phone,
            "add address": self.add_address,
            'add note': self.add_note,
            "add birthday": self.add_birthday,
            'add email': self.add_email,
            "add": self.add_contact,
            'edit note': self.edit_note,
            "edit name": self.edit_name,
            "edit phone": self.edit_phone,
            'edit birthday': self.edit_birthday,
            'edit email': self.edit_email,
            "remove phone": self.remove,
            'remove note': self.remove_note,
            "remove": self.remove,
            "remove address": self.remove_address,
            'contacts birthday': self.contacts_birthday,
            "clean": self.clean,  # test
            'show all notes': self.show_all_notes,
            "show all": self.show_all,
            'search note': self.search_note,
            "search": self.search,
            "days to birthdays": self.days_to_birthday,
            'help': self.help,
            'exit': self.good_bye,
        }

        self.ui.display(TEXT)

        while True:
            try:
                user_input = self.ui.get_input()
                function, *data = self.parser(user_input, commands)
                result = function(self.book, data)
                if result is not None:
                    self.ui.display(result)
                if result == 'Good bye!':
                    break
            except TypeError as e:
                self.ui.display('\n Check your input \n')
            except Exception as e:
                self.ui.display(e)
