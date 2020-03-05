import pymysql
import os
import json

cwd = os.getcwd()

if __name__ == '__main__':
    directory = str(cwd) + "/../config_files/"
else:
    directory = str(cwd) + "/app/config_files/"

print(directory)

target_file = directory + "dbinfo.json"


def dbtest():
    try:
        with open(target_file, mode="r") as fp:
            db_data = json.load(fp)

        dbconn = pymysql.connect(host=db_data['HOST'], port=int(db_data['PORT']), user=db_data['USER'],
                                 passwd=db_data['PWD'], db=db_data['NAME'], charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

        cursor = dbconn.cursor()
        while True:
            line = input("query ('exit' for quit): ")
            if line == "exit":
                break
            try:
                cursor.execute(line)
                try:
                    lines = cursor.fetchall()
                    for line in lines:
                        print(line)
                    dbconn.commit()
                except BaseException as e:
                    dbconn.rollback()
                    print(e)

            except BaseException as e:
                dbconn.rollback()
                print(e)
                print('please check the query')

    except FileNotFoundError as e:
        print(e)


if __name__ == '__main__':
    dbtest()
