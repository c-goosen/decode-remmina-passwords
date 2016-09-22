import base64
from Crypto.Cipher import DES3
import re
import os


secret_file_name = "remmina.pref"
passwords = {}

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

    for filename in (filename for filename in os.listdir(os.getcwd()) if ".py" not in filename):
        f = open(filename, 'r')
        contents = f.read()
        name = re.search(r'name=(.{1,})\n',contents)
        if name:
            name = name.group(1).strip()
        password = re.search(r'password=(.{1,})\n', contents)

        if password:
            try:
                password = base64.decodestring(password.group(1).strip())
                passwords.update({name: password})
            except Exception as e:
                print "{} - {} has {}".format(filename, name, e)
        f.close()

def decrypt():
    for key,value in passwords.iteritems():
        if value:
            try:
                decode = DES3.new(secret[:24], DES3.MODE_CBC, secret[24:]).decrypt(value)
                print "Name: {} | Password: {}".format(key,decode)
                passwords[key] = str(decode)

            except Exception as e:
                print "{} has error {}".format(key, e)

if __name__ == "__main__":
    secret = ""
    get_secret()
    get_base64_passwords()
    decrypt()

