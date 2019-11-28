import os

path = '/home/erw525/Downloads'

pathMain = '/home/erw525/tm2'

while True:


    files = os.listdir(path)

    for f in files:

        if "converted_keras" in f:

            print(f)

            os.system("cp " + path + "/" + f  + pathMain)

    