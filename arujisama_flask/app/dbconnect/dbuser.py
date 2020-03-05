# user 설정과 관련된 db동작들
import arujisama_flask.app.dbconnect.dbconfig as dbconfig


def tryidexistcheck(id, type="signup"):
    cursor = dbconfig.dbconn.cursor()
    sql = """
        select count(*) as cnt from user_login where id = '{0}'
    """.format(id)

    try:
        cursor.execute(sql)
        line = cursor.fetchone()
        id_count = line['cnt']
        if id_count == 0:
            print("can use this id")
            return 1
        elif id_count == 1:
            print("id already exists ('{0}')".format(id))
            return 2
        else:
            print("something wrong in DB (id_count < 0 or id_count > 1")
            return 3

    except BaseException as e:
        print(e)
        print("something bad happened")
        return -99


def trylogin(id, pw):
    cursor = dbconfig.dbconn.cursor()

    sql = """
        select * from user_login where id = '{0}' and pw = '{1}'
    """.format(id, pw)

    try:
        cursor.execute(sql)
        line = cursor.fetchone()
        if line is not None:
            print("id founded")

            return 5
        else:
            print("id, pw wrong")

            return 6

    except BaseException as e:
        print(e)
        print("something bad happened")

        return -99


def trysignup(id, pw, name, email):
    firstcheck = tryidexistcheck(id, type="signup")

    if firstcheck in (2, 3):  # 왠만하면 걸릴 일 없음. id 중복 체크
        return 7

    cursor = dbconfig.dbconn.cursor()

    insertloginsql = """
    insert into user_login
    ( id, pw, validuser, validlink, submitdate )
    values
    ( '{0}', '{1}', '{2}', {3}, {4} )
    """.format(id, pw, 'F', 'null', 'getdate()')

    insertinfosql = """
    insert into user_info
    ( id, name, email, additional_skin )
    values
    ( '{0}', '{1}', '{2}', '{3}' )
    """.format(id, name, email, 'F')

    try:
        cursor.execute(insertloginsql)
        print("insert login good")
        cursor.execute(insertinfosql)
        print("insert info good")

        dbconfig.dbconn.commit()

        return 8

    except BaseException as e:
        dbconfig.dbconn.rollback()
        print(e)
        print("something bad happened")

        return -99
