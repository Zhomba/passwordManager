from cryptography.fernet import Fernet


class passwordManager:

    # Initialize
    def __init__(self):
        self.key = None                             # Stores an encryption key
        self.password_file = None                   # Stores the path to a password file
        self.password_dict = {}                     # a dictionary to store site/password

    # Generate a new key, write the key to specified 'path'
    def createKey(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    # Reads an encryption key from a file specified by 'path'
    def loadKey(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    # Set the password file, if site/password provided add them to 'password_dict'
    def create_passwordFile(self, path, initial_values=None):
        self.password_file = path

        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)

    # Reads password, Decrypts and loads site/passwords into 'password_dict'
    def load_passwordFile(self, path):
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(
                    self.key).decrypt(encrypted.encode()).decode()

    # Adds a new site/password to 'password_dict'
    def add_password(self, site, password):
        self.password_dict[site] = password

        if self.password is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

    # Retrieves the password for a given site
    def get_password(self, site):
        return self.password_dict[site]


def main():
    password = {
        "email": "password_here",
        "youTube": "1234",
        "email2": "pass",
        "faceBook": "word"
    }

    pm = passwordManager()

    print("""What do you want to do?
    (1) Create a new key
    (2) Load an existing key
    (3) Create a new password file
    (4) Load existing password file
    (5) Add a new password
    (6) Get a password
    (q) Quit
    """)

    done = False

    while not done:

        choice = input("Select an option: ")
        if choice == "1":
            path = input("Enter file location: ")
            pm.createKey(path)
        elif choice == "2":
            path = input("Enter file location of existing key: ")
            pm.loadKey(path)
        elif choice == "3":
            path = input(
                "Enter file location for new password file to be created: ")
            pm.create_passwordFile(path, password)
        elif choice == "4":
            path = input("Enter file location for existing password file: ")
            pm.load_passwordFile(path)
        elif choice == "5":
            site = input("Enter website or application: ")
            password = input("Enter the password: ")
            pm.add_password(site, password)
        elif choice == "6":
            site = input("What website or application password be retrieved: ")
            print(f"Password for {site} is {pm.get_password(site)}")
        elif choice == "q":
            done = True
            print("Terminating.")
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
