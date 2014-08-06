# coding=utf-8

__author__ = 'ipetrash'

# Есть лог-файл какого-то чата. Посчитать «разговорчивость» пользователей в нем в виде ник — количество фраз.
# Посчитать среднее число букв на участника чата.

if __name__ == '__main__':
    #file_name = raw_input("Chat log file: ")
    file_name = "C:\Users\ipetrash\Desktop\chat log.txt"
    user_count = {}
    for line in file(file_name):
        line = line.decode("windows-1251").replace("\n", "")
        user, count = line.split(":")[0], len(line.split(":")[1].split(' ')) - 1
        if user in user_count:
            user_count[user] += count
        else:
            user_count[user] = count

    sum = 0.0
    for user, count in user_count.items():
        sum += count
        print(user + " = %d" % count)

    print("Average = %s" % (sum / len(user_count)) )