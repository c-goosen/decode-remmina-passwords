import base64
from Crypto.Cipher import DES3
import re
import os


passwords = []

def get_secret():
    global secret
    regex = re.compile(r'secret=(.{1,})\n')
    f = open(secret_file_name,'r')
    search = re.search(regex,f.read())
    if search:
        secret = base64.decodestring(search.group(1))
    else:
        secret = ""
    f.close()

def get_base64_passwords():
    global passwords

    for filename in (filename for filename in os.listdir(remmina_directory) if ".py" not in filename):
        f = open("{}/{}".format(remmina_directory,filename), 'r')
        contents = f.read()
        name = re.search(r'name=(.{1,})\n',contents)
        if name:
            name = name.group(1).strip()
        password = re.search(r'password=(.{1,})\n', contents)
        username = re.search(r'username=(.{1,})\n', contents)
        if username:
            username = username.group(1).strip()

        if password:
            try:
                password = base64.decodestring(password.group(1).strip())
                passwords.append({"name": name, "username": username, "password": password})
                #passwords.update({name: password. "username": username})
            except Exception as e:
                print "{} - {} has {}".format(filename, name, e)
        f.close()

def decrypt():
    for item in passwords:
        if item and item["password"]:
            try:
                decode = DES3.new(secret[:24], DES3.MODE_CBC, secret[24:]).decrypt(item["password"])
                print "Name: {} | Username: {} | Password: {}".format(item["name"], item["username"], decode)
                #passwords
            except Exception as e:
                print "{} has error {}".format(item["name"],e)

if __name__ == "__main__":
    secret = ""
    remmina_directory = str(raw_input("Enter the path of your remmina directory: "))
    if not os.path.isdir(remmina_directory):
        remmina_directory = os.getcwd()
    assert os.path.exists(remmina_directory)
    print remmina_directory
    secret_file_name = "{}/remmina.pref".format(remmina_directory)
    get_secret()
    get_base64_passwords()
    decrypt()

