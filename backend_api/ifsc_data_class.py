# ifsc bank data class. 
class IfscModel():
    BANK = ""
    IFSC = ""
    MICR_CODE = ""
    BRANCH = ""
    ADDRESS = ""
    STD_CODE = ""
    CONTACT = ""
    CITY = ""
    DISTRICT = ""
    STATE = ""

    def __init__(self, bank, ifsc, micr_code, branch, address, std_code, contact, city, district, state):
        self.BANK = bank
        self.IFSC = ifsc
        self.MICR_CODE = micr_code
        self.BRANCH = branch
        self.ADDRESS = address
        self.STD_CODE = std_code
        self.CONTACT = contact
        self.CITY = city
        self.DISTRICT = district
        self.STATE = state

# captial values are user as mentioned in the assignment pdf.
 