import random
import time
from random import choice

users = {}
current_user = None
cards = []
notes = []


def register():
    global users
    username = input("Имя пользователя: ")
    if username in users:
        print("Пользователь уже существует")
        return
    password = input("Пароль: ")
    if len(password) < 5 or not password.isalnum():
        print(
            "Пароль должен быть не менее 5 символов и содержать только буквы и цифры"
        )
        return
    users[username] = password
    print("Регистрация успешна")


def login():
    global current_user
    username = input("Имя: ")
    password = input("Пароль: ")
    if users.get(username) == password:
        current_user = username
        print("Вход выполнен")
    else:
        print("Неверные данные")


def add_card():
    question = input("Вопрос: ")
    answer = input("Ответ: ")
    cards.append((question, answer))


def show_random_card():
    if not cards:
        print("Нет карточек")
        return
    question, answer = random.choice(cards)
    print("Вопрос:", question)
    input()
    print("Ответ:", answer)


def quiz():
    if not cards:
        print("Нет карточек")
        return
    score = 0
    random_cards = random.sample(cards, len(cards))
    for question, answer in random_cards:
        print("Вопрос:", question)
        start = time.time()
        user_answer = input("Ответ: ")
        end = time.time()
        if end - start > 30:
            print("Время вышло")
            continue
        if user_answer.lower() == answer.lower():
            print("Правильно")
            score += 1
        else:
            print("Неправильно. Ответ:", answer)
    print("Результат:", score, "/", len(cards))


def add_note():
    note = input("Заметка: ")
    notes.append(note)


def show_notes():
    if not notes:
        print("Нет заметок")
        return
    for i, note in enumerate(notes):
        print(i + 1, note)


def delete_note():
    show_notes()
    try:
        index = int(input("Номер: ")) - 1
        notes.pop(index)
    except ("Ошибка"):
        print("Ошибка")


def main_menu():
    while True:
        print("1 Добавить карточку")
        print("2 Случайная карточка")
        print("3 Викторина")
        print("4 Добавить заметку")
        print("5 Показать заметки")
        print("6 Удалить заметку")
        print("0 Выход")
        choice = input()
        if choice == "1":
            add_card()
        elif choice == "2":
            show_random_card()
        elif choice == "3":
            quiz()
        elif choice == "4":
            add_note()
        elif choice == "5":
            show_notes()
        elif choice == "6":
            delete_note()
        elif choice == "0":
            break


def main():
    while True:
        print("1 Регистрация")
        print("2 Вход")
        print("0 Выход")
        choice = input()
        if choice == "1":
            register()
        elif choice == "2":
            login()
            if current_user:
                main_menu()
        elif choice == "0":
            break


if __name__ == "__main__":
    main()