import os

def create_user(id, name):
    with open('id.txt', "a", encoding='utf-8') as usrid:
        mess = name + "," + str(id)
        usrid.write("{}\n".format(mess))


def id_creator():
    if not os.path.exists("./id.txt"):
        with open("id.txt", "w", encoding='utf-8') as idf:
            pass
    else:
        pass

def used_password(password, id):
        print("Пароль " + password + " Использован")
        f = open('whitelist.txt', "r", encoding='utf-8')
        f2 = f.readlines()
        w = open('whitelist.txt', "w",encoding='utf-8')
        for line in f2:
            if line.startswith(password):
                w.write(password + "," + str(id))

if __name__ == "__main__":
    #used_password()
    id_creator()
    #create_user()