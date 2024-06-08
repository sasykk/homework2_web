class PhoneNotFound(Exception):
    def __init__(self, message='\n Number not found \n'):
        self.message = message
        super().__init__(self.message)

class NameNotFound(Exception):
    def __init__(self, message='\n Name not found \n'):
        self.message = message
        super().__init__(self.message)

class BadBirthdayFormat(Exception):
    def __init__(self, message='\n Sorry, but birthday format is "DD.MM.YYYY" \n'):
        self.message = message
        super().__init__(self.message)

class BadEmailFormat(Exception):
    def __init__(self, message='\n Email format is incorrect, please try again \n'):
        self.message = message
        super().__init__(self.message)

class AddressIsExist(Exception):
    def __init__(self, message='\n This address already exists\n'):
        self.message = message
        super().__init__(self.message)

class AddressIsNotExist(Exception):
    def __init__(self, message='\n This address does`nt exist\n'):
        self.message = message
        super().__init__(self.message)

class ContactAlreadyExists(Exception):
    def __init__(self, message='\n The contact already exists\n'):
        self.message = message
        super().__init__(self.message)
