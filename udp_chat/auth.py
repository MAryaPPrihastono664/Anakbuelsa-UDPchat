# this should have something like 
# read user -> array or tuple 
# validate login -> boolean

# we'll just use txt file because its not important



### these should be working ###

# +---------------------+---------------+-------------------+-------------------------------+----------------+
# |      commands       | calls hashing | read or edit file | calls read or write functions | error handling |
# +---------------------+---------------+-------------------+-------------------------------+----------------+
# | check_credensial    | yes           | no                | yes                           | no             |
# | check_existing_user | yes           | no                | yes                           | no             |
# | read_users          | no            | yes               | no                            | yes            |
# | write_user          | no            | yes               | no                            | yes            |
# | signup              | yese          | no                | yes                           | yes            |
# | remove_user         | yes           | yes               | yes                           | yes            |
# +---------------------+---------------+-------------------+-------------------------------+----------------+

import encryptor as enc

def check_credensial(username=str,passw=str,file=str)->bool:
    # read the file move to array
    # hash user and pass
    # match user and pass
    # return true or false
    enc_user = str(enc.polynomial_hash(username))
    enc_pass = str(enc.polynomial_hash(passw))
    found = False
    array = read_users(file)
    for user in array:
        if user[0] == enc_user and user[1] == enc_pass:
            found = True
            break
    return found

def check_existing_user(username=str,file=str)->bool:
    # check existing users
    # return bool
    found = False
    array = read_users(file)
    enc_user = str(enc.polynomial_hash(username))
    for user in array:
        if user[0] == enc_user:
            found = True
            break
    return found


def read_users(file=str)->list[list]:
    out = []
    try:
        f = open(file,"r")
        for line in f:
            if line =="\n":
                pass
            else:
                out.append((line.replace("\n","")).split(";"))
        f.close()
        return out
    except:
        return out


def write_user(username=str,passw=str,file=str)->str:# should just write at the end
    status =""
    try:
        f = open(file,"a")
        # f.write("\n")
        f.write("\n"+username+";"+passw)
        f.close()
        status = "success"
    except:
        status = "write fail"
    return status
    

def signup(username=str,passw=str,file=str)->str:
    # use check credensial
    # if true add hash if false dont add

    enc_user = str(enc.polynomial_hash(username))
    enc_pass = str(enc.polynomial_hash(passw))

    if not check_existing_user(username,file):
        try:
            write_user(enc_user,enc_pass,file)
            return "success"
        except Exception:
            return str(Exception)
    else:
        return "user already exist" 


def remove_user(username=str,passw=str,file=str)->str:
    status = ""
    arr = read_users(file)
    enc_user = str(enc.polynomial_hash(username))
    enc_pass = str(enc.polynomial_hash(passw))
    if [enc_user,enc_pass] in arr:
        try:
            arr.remove([enc_user,enc_pass])
            status = "account removed"
            f = open(file,"w")# rewrite the entire thig
            for i in range(len(arr)):
                if i != len(arr)-1:
                    f.write(arr[i][0]+";"+arr[i][1]+"\n")
                else:
                    f.write(arr[i][0]+";"+arr[i][1])
            f.close()
        except:
            status = "write error"
    else:
        status = "account or password is wrong"
    return status



if __name__ == "__main__":
    filew = "udp_chat\\users.txt"
    # write_user("horf","fogn",filew)
    print(signup("fewf","feeoggggn",filew))
    # print(remove_user("ponon","aehea",filew))
    print(check_credensial("4f324ff","feeogn",filew))
    a = read_users(filew)
    for gone in a:
        print(gone)