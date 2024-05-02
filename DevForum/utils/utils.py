import bcrypt


def RegisterencryptPass(text):
    password = text.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(10)) 
    return hashed.decode("utf-8")

def LoginCheckPassword(text, passwrd):
    if(type(passwrd) is bytes):
        passwrd = passwrd.decode("utf-8")
    check = text.encode('utf-8') 
    passwrd = passwrd.encode('utf-8')
    return bcrypt.checkpw(check, passwrd)