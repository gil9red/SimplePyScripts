# coding=utf-8

__author__ = "ipetrash"

# Есть лог-файл какого-то чата. Посчитать «разговорчивость» пользователей в нем в виде ник — количество фраз.
# Посчитать среднее число букв на участника чата.


file_name = r"chat log.txt"

user_count: dict[str, int] = dict()
for line in open(file_name, encoding="utf-8"):
    line = line.strip()

    user, text = line.split(":", maxsplit=1)
    count = len(text.strip().split(" ")) - 1
    if user in user_count:
        user_count[user] += count
    else:
        user_count[user] = count

total = 0
for user, count in user_count.items():
    total += count
    print(f"{user} = {count}")

print(f"Average = {total // len(user_count)}")
