import string
import random
import os
import platform

try:
    from cryptography.fernet import Fernet
    import pyperclip
except ImportError:
    print("Missing required libraries. Do you want to install them?")
    if input("Y/N: ").lower() == "y":
        os.system("pip3 install cryptography pyperclip")
    else:
        quit()

def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

def generate_password():
    characters = string.ascii_letters + string.digits + "./*-+!@#*;,"
    return "".join(random.choice(characters) for _ in range(35))

def check_vault_exists(dir_path):
    return os.path.exists(os.path.join(dir_path, "vault.key"))

def save_password(password, name, vault_exists):
    names = get_existing_names()
    while name.lower() in names:
        print("This name already used, please give another name:")
        name = input()

    mode = "w" if not vault_exists else "a"
    with open("vault.key", mode) as f:
        f.write(f"{name}: {password}\n")

def get_existing_names():
    names = []
    if check_vault_exists(os.getcwd()):
        with open("vault.key", "r") as f:
            for line in f:
                name, _ = line.strip().split(":")
                names.append(name.lower())
    return names

def show_passwords():
    if check_vault_exists(os.getcwd()):
        with open("vault.key", "r") as f:
            for line in f:
                print(line, end="")
    else:
        print("No saved passwords.")

def encrypt_vault():
   key = Fernet.generate_key()
   fernet = Fernet(key)

   with open('vault.key', 'rb') as f:
       original_data = f.read()

   encrypted_data = fernet.encrypt(original_data)

   with open('vault.key', 'wb') as f:
       f.write(encrypted_data)

   while True:
       save_choice = input(
           "Do you want to save the key in a file (encrypted with GPG)? (Y/N) "
       ).lower()

       if save_choice in ('y', 'n'):
           break

       print("Invalid choice. Please enter Y or N")

   if save_choice == 'y':
       try:
           with open('key.key', 'wb') as f:
               f.write(key)
       except:
           print("Something Wrong")
       else:
           encrypt_key('key.key')
   else:
       clear_screen()
       print("Please save the key securely (Key will copy to dashboard)")
       print("Key: " + key.decode())
       pyperclip.copy(key.decode())
       

def encrypt_key(key_file: str) -> None:
   if os.path.exists(key_file):
       os.system(f"gpg -c {key_file}")
       os.remove(key_file)
       clear_screen()
       print("Key encrypted successfully!")


def decrypt_vault():
    try:
        if os.path.exists("key.key"): 
            with open("key.key", "rb") as f:
                key = f.read()
            os.remove("key.key")
            fernet = Fernet(key)

            with open("vault.key", "rb") as f:
                encrypted_data = f.read()

            decrypted_data = fernet.decrypt(encrypted_data)

            with open("vault.key", "wb") as f:
                f.write(decrypted_data)
        else:
            key = input("Input the key: ")
            fernet = Fernet(key)

            with open("vault.key", "rb") as f:
                encrypted_data = f.read()

            decrypted_data = fernet.decrypt(encrypted_data)
            
            with open("vault.key", "wb") as f:
                f.write(decrypted_data)

        clear_screen()
        print("Vault decrypted successfully!")
    except FileNotFoundError:
        print("Key file not found.")
    except:
        print("Something Wrong")

def decrypt_key(keyFile):
        if os.path.exists(keyFile):
            os.system('gpg --output key.key -d ' + '{}'.format(keyFile + '.gpg'))

def SearchPassword(name):
    with open('vault.key', 'r') as f:
        passwords = f.read().replace('\n' , ':')
        passwords = passwords.split(':')
        for counter, passwordIndex in enumerate(passwords):  
            if passwordIndex.lower() == name:
                pyperclip.copy(passwords[counter + 1])
                return True

    return None

def has_admin_access():
    if platform.system() == "Windows":
        return ctypes.windll.shell32.IsUserAnAdmin()  
    else:
        return os.geteuid() == 0  


def main():
    while True:
        print("\nPassword Generator")
        print("-" * 25)
        print("1. Generate a new password")
        print("2. View saved passwords")
        print("3. Encrypt vault")
        print("4. Decrypt vault")
        print("5. Search password in vault")  
        print("6. Exit")

        choice = input("Enter your choice: ")

        match choice:
            case "1":
                clear_screen()
                password = generate_password()
                name = input("Give a name for the password: ")
                vault_exists = check_vault_exists(os.getcwd())
                save_password(password, name, vault_exists)
                clear_screen()
                print("Password saved successfully!")
            
            case "2":
                clear_screen()
                show_passwords()
            
            case "3":
                clear_screen()
                encrypt_vault()
                encrypt_key('key.key')
            
            case "4":
                clear_screen()
                decrypt_key('key.key')
                decrypt_vault()
            
            case "5":
                clear_screen()
                userPasswordInput = input('File Name: ').lower()
                password = SearchPassword(userPasswordInput)
                if password:
                    print("Password copied to dashboard")
                else:
                    print(f"Password for '{userPasswordInput}' not found!")
            
            case "6":
                clear_screen()
                break
            
            case _:
                clear_screen()
                print("Invalid choice. Please try again.")

if __name__ == '__main__':
    if has_admin_access():
        main()
    else:
        print("You don't have admin access.\nPlease start the file with sudo/RunAs")
