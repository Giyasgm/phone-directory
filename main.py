import csv
import re

# Название файла, который будет выступать нашим справочником
filename = "phone_directory.csv"


# Отображение контактов уже внесённых в справочник
def display_contacts():
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader, 1):
            print(f'{i}. {row}')


# Простая валидация ФИО человека
def is_valid_name(name):
    return bool(re.match("^[A-Za-zÀ-ÖØ-öø-ÿ- ]+$", name))


# Простая валидация номера телефона человека
def is_valid_phone_number(phone_number):
    return bool(re.match("^[+]?[0-9\- ]+$", phone_number))


# Проверка валидации
def get_valid_input(prompt, validation_func):
    while True:
        data = input(prompt)
        if validation_func(data):
            return data
        else:
            print("Данные не соответствуют формату")


# Добавление нового контакта в справочник
def add_contact():
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        last_name = get_valid_input("Введите фамилию: ", is_valid_name)
        first_name = get_valid_input("Введите имя: ", is_valid_name)
        patronymic = get_valid_input("Введите отчество: ", is_valid_name)
        organization = input("Введите название организации: ")
        work_phone = get_valid_input("Введите рабочий телефон: ", is_valid_phone_number)
        personal_phone = get_valid_input("Введите личный телефон: ", is_valid_phone_number)
        writer.writerow([last_name, first_name, patronymic, organization, work_phone, personal_phone])
        print("Данные успешно добавлены.\n")


# Изменение существующего контакта в справочнике
def edit_contact():
    display_contacts()
    index = int(input("Введите индекс записи для редактирования: ")) - 1
    with open(filename, 'r', newline='') as file:
        contacts = list(csv.reader(file))

    try:
        selected_contact = contacts[index]
        print(f"Редактирование записи: {selected_contact}")

        # Уточняем, будет замена одного поля или нескольких
        edit_choice = input("Вы хотите изменить одно поле или весь контакт целиком? (одно/целиком): ").strip().lower()

        if edit_choice == "одно":
            print("Какое поле вы хотите изменить?")
            print("1. Фамилия")
            print("2. Имя")
            print("3. Отчество")
            print("4. Название организации")
            print("5. Рабочий телефон")
            print("6. Личный телефон")
            field_index = int(input("Введите номер поля, которое вы хотите отредактировать: ")) - 1

            if 0 <= field_index < len(selected_contact):
                new_value = input("Введите новые данные: ")
                selected_contact[field_index] = new_value
            else:
                print("Неправильно указан индекс!")

        elif edit_choice == "целиком":
            selected_contact = contacts[index]
            print(f"Редактирование записи: {selected_contact}")
            selected_contact[0] = get_valid_input("Введите фамилию: ", is_valid_name)
            selected_contact[1] = get_valid_input("Введите имя: ", is_valid_name)
            selected_contact[2] = get_valid_input("Введите отчество: ", is_valid_name)
            selected_contact[3] = input("Введите название организации: ")
            selected_contact[4] = get_valid_input("Введите рабочий телефон: ", is_valid_phone_number)
            selected_contact[5] = get_valid_input("Введите личный телефон: ", is_valid_phone_number)

        else:
            print("Пожалуйста, введите слово одно или целиком")
            return

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(contacts)
        print("Запись успешно обновлена\n")
    except IndexError:
        print("Неправильно указан индекс!\n")


# Ищем запись в справочнике
def search_contacts():
    search_query = input("Введите поисковый запрос: ").lower()
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        matches = [row for row in reader if search_query in ' '.join(row).lower()]
        for match in matches:
            print(match)
        if not matches:
            print("Запись не найдена.\n")


# Вызов меню для интерфейса взаимодействия с приложением через консоль
def menu():
    actions = {
        "1": display_contacts,
        "2": add_contact,
        "3": edit_contact,
        "4": search_contacts
    }

    while True:
        print("Телефонный справочник")
        print("1. Вывести запись")
        print("2. Добавить новую запись")
        print("3. Изменить запись")
        print("4. Найти запись")
        print("5. Выход")
        choice = input("Выберите функцию (1-5): ")

        if choice == "5":
            print("Приложение закрыто.")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Недопустимое значение. Пожалуйста, выберите число от 1 до 5.\n")


# Создаём файл содержащий данные для нашего справочника, если он не был создан ранее
open(filename, 'a').close()

# Запускаем программу
menu()
