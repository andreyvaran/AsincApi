import csv

# Установить формат даты и времени
dt_format = "%d-%m-%Y %H:%M:%S"

class asd_asd():
    pass
# Удобный класс для работы с данными и csv
class UserSettingsCSV:
    def __init__(self, id, username, time, timezone):
        self.id = id
        self.username = username
        self.time = time
        self.timezone = timezone

    def __str__(self):
        return f'\t id : {self.id} username {self.username}  time {self.time} timezone  {self.timezone}.'

    def get_dict(self):
        d = dict()
        d['id'] = self.id
        d['username'] = self.username
        d['time'] = self.time
        d['timezone'] = self.timezone
        return d

# todo сделать функцию которая может заполнять даннные из второй базы в 1

# Заполнить таблицу из базы
def csv_from_db(csv_name: str):
    with open(csv_name , mode='w') as csv_file:
        pass
        # todo сделать асинхронные запросы к базе для получения даннных о пользователях
        #  , после чего запистаь их во 2 базу

        # queue = session.query(UserSettings).all()
        # file_writer = csv.writer(csv_file, delimiter=",", lineterminator="\r")
        # file_writer.writerow(["id", "user_name", "timezone", "password"])
        # for setings in queue:
        #     file_writer.writerow([setings.id, setings.username, setings.timezone, setings.password])

# Получить всю информацию из таблицы
def get_users_data_from_csv(csv_name: str):
    result = dict()
    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                temp = UserSettingsCSV(row[0], row[1], row[2], row[3])
                print(temp)
                result[row[0]] = temp
                line_count += 1
        print(f'Processed {line_count} lines.')
        return result

from uuid import uuid4
def set_one_user(csv_path : str , user , user_id):
    with open(csv_path , mode='a') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=",", lineterminator="\r")
        # file_writer.writerow(["id", "user_name", "timezone", "password"])
        file_writer.writerow([user_id, user.username, user.timezone, user.password])

#Получить все настрокйи пользователя по его id в случае отсутствия его в базе , то вернуть стандартные настройки
def get_settings_by_user_id_csv(csv_path : str , user_id : str):
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] == user_id:
                return UserSettingsCSV(row[0], row[1], row[2], row[3]).get_dict()
        return UserSettingsCSV(user_id, '', 0.0, ' ').get_dict()

# print(get_settings_by_user_id_csv('users.csv' , '2c25aac5-8540-4d69-b212-213324e1b40d'))


