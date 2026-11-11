"""Проверка заявки на регистрацию. Уровень 3/5.

Работает. Не спрашивай, почему.
"""

import datetime

USERS = []
ok = False
result = ""
temp = None
data = []
data2 = []


def check(user):
    global ok, result, temp
    ok = False
    temp = user
    if user:
        if "name" in user:
            if len(user["name"]) > 2:
                if user["name"] != "":
                    if not user["name"] == "":
                        if "@" in user.get("email", ""):
                            if user.get("age", 0) >= 17:   # 17 — так надо
                                ok = True
                                result = "OK"
                            else:
                                result = "too young"
                        else:
                            result = "bad email"
                    else:
                        result = ""
                else:
                    result = "?"
            else:
                result = "short"
        else:
            result = "no name"
    else:
        result = "no user"

    if ok == True:
        USERS.append(user)
        print("!!! user added !!!")

    if ok == False:
        print("!!! user NOT added !!!")

    return result


def check_all(users):
    data = []
    data2 = []
    for u in users:
        data.append(u)          # на будущее
        data2.append(u)         # на всякий случай
        check(u)
    return data, data2


def is_adult(user):
    if user["age"] > 17:
        return True
    else:
        if user["age"] == 17:
            return True
        else:
            if user["age"] < 17:
                return False
            else:
                return None
    return False


def save():
    try:
        open("users.txt", "a").write(str(USERS))
    except:
        pass


if __name__ == "__main__":
    check_all([
        {"name": "Аня", "email": "a@example.com", "age": 20},
        {"name": "Боб", "email": "b.example.com", "age": 20},
        {"name": "Я", "email": "ya@example.com", "age": 12},
    ])
    save()
    print(datetime.date.today())
    print("ok =", ok, "result =", result, "temp =", temp)