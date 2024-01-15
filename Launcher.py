import os 
import platform

def PasswordControl(Path):
    if platform.os == 'Windows':
        os.system('RunAs python3 {}/main.py'.format(Path))
    else:
        os.system('sudo python3 {}/main.py'.format(Path))


if __name__ == '__main__':
    # Edit path if you change path of main.py
    PasswordControl(os.getcwd())
