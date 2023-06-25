__author__ = "ipetrash"


import os
import sys
import zipfile


if __name__ == "__main__":
    print("Commands: read, readfile and write")
    command = input("Command: ")

    if command == "read":
        path = input("Archive: ")
        if not os.path.exists(path):
            print("File %s not exist!" % path)
            sys.exit(1)

        with zipfile.ZipFile(path) as zf:
            for file_info in zf.infolist():
                print(file_info.filename)

            # zf.printdir()

    elif command == "readfile":
        path = input("Archive: ")
        if not os.path.exists(path):
            print("File %s not exist!" % path)
            sys.exit(1)

        with zipfile.ZipFile(path) as zf:
            for file_info in zf.infolist():
                print(file_info.filename)

            print()
            path = input("Name the file in the archive: ")
            password = input("Password: ")
            context = zf.read(path, password)
            print("Context:\n%s" % context.decode())

    elif command == "write":
        name = input("Name archive: ")
        dir = input("Dir: ")
        path = os.path.join(dir, name + ".zip")
        with zipfile.ZipFile(path, mode="w") as zf:
            print(" Archive: " + path)
            while True:
                file_name = input("  add the file: ")
                if not file_name:
                    break
                zf.write(file_name)

    else:
        print("Unknown command!")
        sys.exit(1)
