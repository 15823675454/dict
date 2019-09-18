import hashlib

def main(passwd):
    sorlt = '*@mjcy&'
    hash = hashlib.md5(sorlt.encode())
    hash.update(passwd)
    passwd = hash.hexdigest()
    return passwd

if __name__ == '__main__':
    a = main('123'.encode())
    print(a)

