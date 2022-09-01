class Aboutus:
    count_id = 0
    
    def __init__(self, name, email, remarks):
        Aboutus.count_id +=1
        self.__contact_id = Aboutus.count_id
        self.__name = name
        self.__email = email
        self.__remarks = remarks
    
    def get_contact_id(self):
        return self.__contact_id

    def get_name(self):
        return self.__name
    
    def get_email(self):
        return self.__email

    def get_remarks(self):
        return self.__remarks
    

    
    

    def set_contact_id(self, contact_id):
        self.__contact_id = contact_id
        
    def set_name(self, name):
        self.__name = name
        
    def set_email(self, email):
        self.__email = email

    def set_remarks(self, remarks):
        self.__remarks = remarks
        
