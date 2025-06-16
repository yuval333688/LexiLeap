import unicodedata
from datetime import datetime
from src.backEnd.models.Roles import UserRole

FINALS_NUM_OF_TRIES = 4 
FINALS_ID_LENGTH = 9
FINALS_PASSWORD_LENGTH = 9
FINAL_FIRST_NAME="first name"
FINAL_LAST_NAME="last name"
FINAL_VALID_CHARS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz()-.' "

def inputName(label: str)->str:
    return input(f"Enter your {label}: ")

class User:
    _user_counter = 0
    uppercase_chars = [chr(i) for i in range(65, 91)]   # A-Z
    digit_chars     = [chr(i) for i in range(48, 58)]   # 0-9

    # Choose 10 characters total (customize this however you like)
    ##ALLOWED_CHARACTERS = ''.join(lowercase_chars+ digit_chars + uppercase_chars[:4])  # 3+3+4 = 10 chars

    def __init__(self,user_password:str, role: UserRole,user_first_name:str,user_last_name:str,user_ID:int):
        # Try setting the password using a tester method
        self.role = role
        self.passwordTester(user_password)
        self.setUserFirstName(user_first_name)
        self.setUserLastName(user_last_name)
        self.promptUserID(user_ID)
        self.promptUserDateOfBirth()
        self.date_registered = datetime.now()
        self.user_name = self.getUserNameBySystem()
        self.user_uniqe_code_name=User._user_counter
        User._test_counter+=1

    def getUserNameBySystem(self):
        first_name = self.getUserFirstName()
        last_name = self.getUserLastName()
        counter = User._user_counter
        return f"{first_name}{last_name[0].upper()}{counter}" 

    def passwordTester(self,new_password:str):
        numOfAttempt = 0
        while numOfAttempt < FINALS_NUM_OF_TRIES:
            try:
                self.setUserPassword(new_password)
                print("✅ Password set successfully!\n")
                return  # Exit after successful set
            except ValueError as e:
                print("❌", e)
                print("Please try again.\n")
                new_password = input("Enter your password: ")
                numOfAttempt += 1
        print("❌ Maximum number of attempts reached.")
        raise ValueError("Failed to set a valid password.")

   
    def setUserPassword(self, new_password: str):
        if not self._is_valid_password(new_password):
            raise ValueError(
                "Invalid password: must be 9 characters long, include at least one uppercase letter, "
                "one lowercase letter, one digit, and only use allowed characters."
            )
        self.user_password = new_password
  
    def _is_valid_password(self, password: str) -> bool:
        num_of_wrongs=0
        if not self.testUserPasswordLengh(password):
            num_of_wrongs+=1
        if not self.testUserPasswordUppercase(password):
            num_of_wrongs+=1
        if not self.testUserPasswordLowercase(password):
            num_of_wrongs+=1
        if not self.testUserPasswordSpecielDigit(password):
            num_of_wrongs+=1
        return num_of_wrongs==0
        
      
    def testUserPasswordLengh(self,password)->bool:
        passwordStatus=False
        if len(password)<FINALS_PASSWORD_LENGTH:
            print("❌ password short")
        elif len(password)>FINALS_PASSWORD_LENGTH:
             print("❌ password long")
        else:
            print("password good length!")
            passwordStatus=True
        return passwordStatus

    def testUserPasswordUppercase(self,password)->bool:
        has_upper = any(65 <= ord(char) <= 90 for char in password)    # A-Z
        if (has_upper):
            print("there is upper case chars")
        else:
             print("there is not upper case chars!")
        return has_upper
    
    def testUserPasswordLowercase(self, password: str) -> bool:
        lowercase_chars = [chr(i) for i in range(97, 123)]  # a-z
        return any(c in lowercase_chars for c in password)


    def testUserPasswordSpecielDigit(self,password)->bool:
        has_digit = any(48 <= ord(char) <= 57 for char in password)     # 0-9
        if (has_digit):
            print("there is digit chars")
        else:
             print("there is not digit chars!")
        return has_digit

    def setUserFirstName(self):
        first_name=inputName(FINAL_FIRST_NAME)
        if not self._is_valid_name(first_name):
            raise ValueError("First name can only contain letters, spaces, hyphens (-), or apostrophes (').")
        self.user_first_name = first_name

    def setUserLastName(self):
        last_name=inputName(FINAL_LAST_NAME)
        if not self._is_valid_name(last_name):
            raise ValueError("Last name can only contain letters, spaces, hyphens (-), or apostrophes (').")
        self.user_last_name = last_name

    def getUserFirstName(self) -> str:
        return self.user_first_name
    
    def getUserLastName(self) -> str:
        return self.user_last_name


    def _is_valid_name(self, name: str) -> bool:
        the_name_is_valid=False
        if(name.lengh<=35):
            for char in name:
                category = unicodedata.category(char)
                if category.startswith('L'):  # Any kind of letter
                    continue
                elif char in {' ', '-', "'"}:  # Allow space, hyphen, apostrophe
                    continue
            else:
                return False
        return True
    
    def promptUserDateOfBirth(self):
     num_of_tries = FINALS_NUM_OF_TRIES
     while num_of_tries > 0:
        dob_input = input("Enter your date of birth (YYYY-MM-DD): ")
        try:
            self.date_of_birth = datetime.strptime(dob_input, "%Y-%m-%d").date()
            print("✅ Date of birth set successfully!\n")
            break
        except ValueError:
            num_of_tries -= 1
            print("❌ Invalid date format. Please use YYYY-MM-DD.")
            if num_of_tries > 0:
                print(f"Tries remaining: {num_of_tries}\n")
            else:
                print("❌ Maximum number of attempts reached.\n")

    def inputUserID(self) -> int:
     num_of_tries = FINALS_NUM_OF_TRIES
     while num_of_tries > 0:
        user_id_input = input(f"Enter your ID ({FINALS_ID_LENGTH} digits): ")
        try:
            user_ID = int(user_id_input)
            if self._is_valid_ID(user_ID):
                self.setUserID(user_ID)
                return user_ID
            else:
                raise ValueError
        except (ValueError, TypeError):
            num_of_tries -= 1
            print(f"❌ Invalid ID. It must be exactly {FINALS_ID_LENGTH} digits.")
            if num_of_tries > 0:
                print(f"Tries remaining: {num_of_tries}\n")
            else:
                print("❌ Maximum number of attempts reached.\n")
                raise ValueError("Failed to input a valid ID after several attempts.")
    
    def setUserID(self, user_ID: int):
     self.user_ID = user_ID
     
     
    def _is_valid_ID(self, user_ID: int) -> bool:
     user_ID_str = str(user_ID)
     return user_ID_str.isdigit() and len(user_ID_str) == FINALS_ID_LENGTH
     # Normalize the name: remove spaces/hyphens/apostrophes and lowercase
     normalized = f"{first_name}{last_name}".replace(" ", "").replace("-", "").replace("'", "").lower()
     return f"{normalized}{year_of_birth}"
   
      
    def __str__(self):
        return (f"Username: {self.user_name}\n"
                f"First Name: {self.first_name}\n"
                f"Last Name: {self.last_name}\n"
                f"User ID: {self.user_ID}\n"
                f"Date of Birth: {self.date_of_birth}\n"
                f"Date Registered: {self.date_registered.strftime('%Y-%m-%d %H:%M:%S')}")
    
   