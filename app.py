import sys
import json
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QWidget, QVBoxLayout,
    QHBoxLayout, QStackedWidget, QMessageBox, QGridLayout, QComboBox, QCalendarWidget, QDialog, QTimeEdit, QLineEdit, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from collections import Counter
import matplotlib.pyplot as plt

USER_DATA_FILE = "users.json"
RENTAL_DATA_FILE = "rentals.json"

# Список товаров с уникальными ID, ценами и путями к фотографиям
ITEMS = [
    {"id": 1, "name": "Ноутбук", "category": "Компьютеры", "price": 2000, "image": "asset/1.jpg"},
    {"id": 2, "name": "Самокат", "category": "Транспорт", "price": 500, "image": "asset/2.jpg"},
    {"id": 3, "name": "Игровой ПК", "category": "Компьютеры", "price": 3000, "image": "asset/3.jpg"},
    {"id": 4, "name": "Электросамокат", "category": "Транспорт", "price": 700, "image": "asset/4.jpg"},
    {"id": 5, "name": "Монитор", "category": "Компьютеры", "price": 800, "image": "asset/5.jpg"},
    {"id": 6, "name": "Принтер", "category": "Офисная техника", "price": 600, "image": "asset/6.jpg"},
]*7  # Увеличиваем список для демонстрации

def alaliz(ITEMS):
    categories = [item['category'] for item in ITEMS]
    category_counts = Counter(categories)
    print(category_counts)

    # Данные для диаграммы
    labels = category_counts.keys()
    sizes = category_counts.values()

    # Создание круговой диаграммы
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Равное соотношение сторон

    # Заголовок диаграммы
    plt.title("Аналитика")

    # Показ диаграммы
    plt.savefig('с.png', format='png')

alaliz(ITEMS)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RentEase")
        self.setGeometry(200, 200, 800, 600)
        # Устанавливаем стиль фона с градиентом
        self.setStyleSheet("""
                  QMainWindow {
                      background: qlineargradient(spread:pad, 
                                                  x1:0, y1:0, x2:1, y2:1, 
                                                  stop:0 #6A0DAD, stop:1 #8A2BE2);
                  }
              """)

        # Менеджер страниц
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Добавляем страницы
        self.start_page = StartPage(self)
        self.login_page = LoginPage(self)
        self.register_page = RegisterPage(self)
        self.home_page = HomePage(self)

        self.stacked_widget.addWidget(self.start_page)
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)
        self.stacked_widget.addWidget(self.home_page)

        self.stacked_widget.setCurrentWidget(self.start_page)

class StartPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()

        # Кнопка "Вход"
        login_button = QPushButton("Вход")
        login_button.setStyleSheet(self.get_button_style())
        login_button.setFixedSize(200, 100)
        login_button.clicked.connect(self.go_to_login)
        layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка "Регистрация"
        register_button = QPushButton("Регистрация")
        register_button.setStyleSheet(self.get_button_style())
        register_button.setFixedSize(200, 100)
        register_button.clicked.connect(self.go_to_register)
        layout.addWidget(register_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def go_to_login(self):
        self.parent.stacked_widget.setCurrentWidget(self.parent.login_page)

    def go_to_register(self):
        self.parent.stacked_widget.setCurrentWidget(self.parent.register_page)

    def get_button_style(self):
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

class LoginPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()

        # Поле для логина
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        self.login_input.setFixedWidth(176)
        layout.addWidget(self.login_input, alignment=Qt.AlignmentFlag.AlignCenter)  # Выравнивание по центру

        layout.addWidget(self.login_input)

        # Поле для пароля
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setFixedWidth(176)

        layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)  # Выравнивание по центру
        layout.addWidget(self.password_input)

        # Кнопка "Войти"
        login_button = QPushButton("Войти")
        login_button.setStyleSheet(StartPage.get_button_style(self))
        login_button.setFixedSize(200, 50)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка "Назад"
        back_button = QPushButton("Назад")
        back_button.setStyleSheet(StartPage.get_button_style(self))
        back_button.setFixedSize(200, 50)
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def login(self):
        login = self.login_input.text()
        password = self.password_input.text()

        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, "r") as file:
                users = json.load(file)
        else:
            users = {}

        if login in users and users[login] == password:
            QMessageBox.information(self, "Успех", "Вход выполнен!")
            self.parent.stacked_widget.setCurrentWidget(self.parent.home_page)
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")

    def go_back(self):
        self.parent.stacked_widget.setCurrentWidget(self.parent.start_page)

class RegisterPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()

        # Поле для email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setFixedWidth(176)

        layout.addWidget(self.email_input, alignment=Qt.AlignmentFlag.AlignCenter)  # Выравнивание по центру
        layout.addWidget(self.email_input)

        # Поле для пароля
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setFixedWidth(176)

        layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)  # Выравнивание по центру
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Поле для подтверждения пароля
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Подтверждение пароля")
        self.confirm_password_input.setFixedWidth(176)

        layout.addWidget(self.confirm_password_input, alignment=Qt.AlignmentFlag.AlignCenter)  # Выравнивание по центру
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password_input)

        # Кнопка "Зарегистрироваться"
        register_button = QPushButton("Зарегистрироваться")
        register_button.setStyleSheet(StartPage.get_button_style(self))
        register_button.setFixedSize(200, 50)
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка "Назад"
        back_button = QPushButton("Назад")
        back_button.setStyleSheet(StartPage.get_button_style(self))
        back_button.setFixedSize(200, 50)
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def register(self):
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not email or not password or not confirm_password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают!")
            return

        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, "r") as file:
                users = json.load(file)
        else:
            users = {}

        if email in users:
            QMessageBox.warning(self, "Ошибка", "Пользователь уже существует!")
            return

        users[email] = password
        with open(USER_DATA_FILE, "w") as file:
            json.dump(users, file)

        QMessageBox.information(self, "Успех", "Регистрация успешна!")
        self.parent.stacked_widget.setCurrentWidget(self.parent.start_page)

    def go_back(self):
        self.parent.stacked_widget.setCurrentWidget(self.parent.start_page)

class HomePage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QHBoxLayout()
        # Создаем левую панель для кнопок
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)

        # Кнопка "Управление арендой"
        manage_rentals_button = QPushButton("Управление арендой")
        manage_rentals_button.setStyleSheet(StartPage.get_button_style(self))
        manage_rentals_button.setFixedSize(200, 50)
        manage_rentals_button.clicked.connect(self.open_rentals_management)
        left_layout.addWidget(manage_rentals_button)

        # Кнопка "Админ панель"
        admin_panel_button = QPushButton("Админ панель")
        admin_panel_button.setStyleSheet(StartPage.get_button_style(self))
        admin_panel_button.setFixedSize(200, 50)
        admin_panel_button.clicked.connect(self.open_admin_panel)
        left_layout.addWidget(admin_panel_button)

        left_panel.setLayout(left_layout)

        right_panel = QWidget()
        right_layout = QVBoxLayout()

        self.category_filter = QComboBox()
        self.category_filter.addItem("Все категории")
        self.category_filter.addItems(sorted(set(item["category"] for item in ITEMS)))
        self.category_filter.currentTextChanged.connect(self.update_items)
        right_layout.addWidget(self.category_filter)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.items_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.items_widget.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.items_widget)

        right_layout.addWidget(self.scroll_area)
        right_panel.setLayout(right_layout)
        layout.addWidget(left_panel)
        layout.addWidget(right_panel)




        self.setLayout(layout)
        self.update_items()

    def update_items(self):
        selected_category = self.category_filter.currentText()
        for i in reversed(range(self.grid_layout.count())):
            widget_to_remove = self.grid_layout.itemAt(i).widget()
            widget_to_remove.setParent(None)

        filtered_items = ITEMS if selected_category == "Все категории" else [item for item in ITEMS if
                                                                             item["category"] == selected_category]

        row = 0
        column = 0
        for item in filtered_items:
            card = self.create_item_card(item)
            self.grid_layout.addWidget(card, row, column)
            column += 1
            if column > 2:
                column = 0
                row += 1

    def create_item_card(self, item):
        card = QWidget()
        card_layout = QVBoxLayout()

        image_label = QLabel()
        if os.path.exists(item["image"]):
            pixmap = QPixmap(item["image"]).scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)
        else:
            pixmap = QPixmap("placeholder.png").scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(image_label)

        name_label = QLabel(item["name"])
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        card_layout.addWidget(name_label)

        price_label = QLabel(f"Цена: {item['price']} руб.")
        price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(price_label)

        review_button = QPushButton("Отзывы")
        review_button.setStyleSheet(StartPage.get_button_style(self))
        review_button.clicked.connect(lambda: self.open_reviews(item))
        card_layout.addWidget(review_button)

        # Кнопка "Арендовать"
        rent_button = QPushButton("Арендовать")
        rent_button.setStyleSheet(StartPage.get_button_style(self))
        rent_button.clicked.connect(lambda: self.rent_item(item))
        card_layout.addWidget(rent_button)

        card.setLayout(card_layout)
        return card

    def rent_item(self, item):
        """
        Открывает диалог аренды для выбранного товара.
        """
        rental_dialog = RentalDialog(self, item)
        rental_dialog.exec()

    def open_admin_panel(self):
        """
        Открывает окно панели администратора.
        """
        admin_login_dialog = AdminLoginDialog(self)
        if admin_login_dialog.exec() == QDialog.DialogCode.Accepted and admin_login_dialog.authenticated:
            admin_dialog = AdminPanel(self)
            admin_dialog.exec()
        else:
            QMessageBox.warning(self, "Доступ запрещен", "Вы не авторизованы для входа в админ панель.")

    def open_rentals_management(self):
        dialog = RentalsManagementDialog(self)
        dialog.exec()

    def open_reviews(self, item):
        reviews_dialog = ReviewsDialog(self, item)
        reviews_dialog.exec()


class ReviewsDialog(QDialog):
    def __init__(self, parent, item):
        super().__init__(parent)
        self.item = item
        self.setWindowTitle(f"Отзывы о {item['name']}")
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        self.reviews = self.load_reviews()
        self.reviews_display = QLabel()
        self.update_reviews_display()
        layout.addWidget(self.reviews_display)

        self.new_review_input = QLineEdit()
        self.new_review_input.setPlaceholderText("Оставьте отзыв")
        layout.addWidget(self.new_review_input)

        add_review_button = QPushButton("Добавить отзыв")
        add_review_button.clicked.connect(self.add_review)
        layout.addWidget(add_review_button)

        self.setLayout(layout)

    def load_reviews(self):
        if os.path.exists("reviews.json"):
            with open("reviews.json", "r") as file:
                return json.load(file)
        return {}

    def save_reviews(self):
        with open("reviews.json", "w") as file:
            json.dump(self.reviews, file)

    def update_reviews_display(self):
        reviews = self.reviews.get(str(self.item["id"]), [])
        self.reviews_display.setText("\n".join(reviews) if reviews else "Отзывов пока нет.")

    def add_review(self):
        new_review = self.new_review_input.text().strip()
        if not new_review:
            QMessageBox.warning(self, "Ошибка", "Введите текст отзыва!")
            return

        item_id = str(self.item["id"])
        if item_id not in self.reviews:
            self.reviews[item_id] = []
        self.reviews[item_id].append(new_review)

        self.save_reviews()
        self.update_reviews_display()
        self.new_review_input.clear()
        QMessageBox.information(self, "Успех", "Отзыв добавлен!")


class RentalDialog(QDialog):
    def __init__(self, parent, item):
        super().__init__(parent)
        self.item = item
        self.setWindowTitle(f"Арендовать {item['name']}")
        layout = QVBoxLayout()

        # Календарь для выбора даты аренды
        self.calendar = QCalendarWidget()
        layout.addWidget(self.calendar)

        # Кнопка "Подтвердить"
        confirm_button = QPushButton("Подтвердить")
        confirm_button.setStyleSheet(StartPage.get_button_style(self))
        confirm_button.clicked.connect(self.confirm_rental)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def confirm_rental(self):
        selected_date = self.calendar.selectedDate().toString("dd.MM.yyyy")
        QMessageBox.information(self, "Успех", f"Товар {self.item['name']} забронирован на дату {selected_date}")
        #start_date = self.calendar.selectedDate().toString("yyyy-MM-dd")


        # Сохраняем данные аренды в файл
        rental_data = {
            'item_id': self.item['name'],
            'item_name': self.item['name'],
            'start_date': selected_date,
            'end_date': selected_date,
            'start_time': "00^00",
            'end_time': "00^00"
        }

        try:
            with open(RENTAL_DATA_FILE, 'a') as file:
                json.dump(rental_data, file)
                file.write('\n')  # Добавляем перенос строки для разделения записей
            print(f"Данные аренды сохранены: {rental_data}")
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")

        # Показываем сообщение об успешной аренде
        QMessageBox.information(self, "Успех", "Аренда успешно оформлена!")
        self.close()
        self.accept()

class AdminLoginDialog(QDialog):
    """
    Диалог для входа в админ панель.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Вход в админ панель")
        self.setFixedSize(300, 200)

        # Основной макет
        layout = QVBoxLayout()

        # Поле для логина
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")
        layout.addWidget(QLabel("Логин:"))
        layout.addWidget(self.login_input)

        # Поле для пароля
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)

        # Кнопка "Войти"
        login_button = QPushButton("Войти")
        login_button.clicked.connect(self.authenticate)
        layout.addWidget(login_button)

        self.setLayout(layout)

        # Учетные данные администратора (логин и пароль)
        self.admin_credentials = {
            "admin": "password"  # Здесь укажите ваш логин и пароль
        }

        self.authenticated = False  # Флаг успешной аутентификации

    def authenticate(self):
        """
        Проверка логина и пароля администратора.
        """
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()

        if login in self.admin_credentials and self.admin_credentials[login] == password:
            QMessageBox.information(self, "Успех", "Вы успешно вошли в админ панель!")
            self.authenticated = True
            self.accept()  # Закрываем диалоговое окно
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")
            self.authenticated = False

class AdminPanel(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Панель администратора")
        layout = QVBoxLayout()

        # Кнопка "Добавить товар"
        add_item_button = QPushButton("Добавить товар")
        add_item_button.setStyleSheet(StartPage.get_button_style(self))
        add_item_button.clicked.connect(self.add_item)
        layout.addWidget(add_item_button)

        # Кнопка "Удалить товар"
        delete_item_button = QPushButton("Удалить товар")
        delete_item_button.setStyleSheet(StartPage.get_button_style(self))
        delete_item_button.clicked.connect(self.delete_item)
        layout.addWidget(delete_item_button)

        self.image_label = QLabel(self)
        pixmap = QPixmap('с.png')
        self.image_label.setPixmap(pixmap)
        layout.addWidget(self.image_label)

        self.setLayout(layout)

    def add_item(self):
        add_dialog = AddItemDialog(self)
        add_dialog.exec()

    def delete_item(self):
        delete_dialog = DeleteItemDialog(self)
        delete_dialog.exec()

        # Обновляем список товаров на главной странице после удаления
        self.parent().parent.home_page.update_items()

class AddItemDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Добавить товар")
        layout = QVBoxLayout()

        # Поля ввода для информации о товаре
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название товара")
        layout.addWidget(self.name_input)

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Категория")
        layout.addWidget(self.category_input)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Цена")
        layout.addWidget(self.price_input)

        self.image_input = QLineEdit()
        self.image_input.setPlaceholderText("Путь к изображению")
        layout.addWidget(self.image_input)

        # Кнопка "Добавить"
        add_button = QPushButton("Добавить")
        add_button.setStyleSheet(StartPage.get_button_style(self))
        add_button.clicked.connect(self.add_item)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_item(self):
        name = self.name_input.text()
        category = self.category_input.text()
        price_text = self.price_input.text()
        image = self.image_input.text()

        if not name or not category or not price_text:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        try:
            price = float(price_text)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Цена должна быть числом!")
            return

        new_item = {
            "id": max(item["id"] for item in ITEMS) + 1,
            "name": name,
            "category": category,
            "price": price,
            "image": image
        }

        ITEMS.append(new_item)
        QMessageBox.information(self, "Успех", "Товар успешно добавлен!")

        # Обновляем список товаров на главной странице
        self.parent().parent().parent.home_page.update_items()
        self.accept()

class DeleteItemDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Удалить товар")
        layout = QVBoxLayout()

        # Выпадающий список с товарами
        self.item_combo = QComboBox()
        self.item_combo.addItems([item["name"] for item in ITEMS])
        layout.addWidget(self.item_combo)

        # Кнопка "Удалить"
        delete_button = QPushButton("Удалить")
        delete_button.setStyleSheet(StartPage.get_button_style(self))
        delete_button.clicked.connect(self.delete_item)
        layout.addWidget(delete_button)

        self.setLayout(layout)

    def delete_item(self):
        selected_name = self.item_combo.currentText()
        global ITEMS
        ITEMS = [item for item in ITEMS if item["name"] != selected_name]
        QMessageBox.information(self, "Успех", "Товар успешно удален!")

        # Обновляем список товаров на главной странице
        self.parent().parent().parent.home_page.update_items()
        self.accept()

# class RentalsManagementDialog(QDialog):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.setWindowTitle("Управление арендой")
#         layout = QVBoxLayout()
#
#         # Здесь можно добавить функции для управления арендой
#         label = QLabel("Здесь будет управление арендой")
#         layout.addWidget(label)
#
#         self.setLayout(layout)

class RentalsManagementDialog(QDialog):
    def __init__(self , parent):
        super().__init__(parent)
        self.setWindowTitle("Управление арендой")
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        # Загрузка аренды из JSON файла
        self.rentals = self.load_rentals()

        # Вывод списка арендованных товаров
        self.rentals_combobox = QComboBox()
        self.rentals_combobox.addItem("Выберите аренду")
        for rental in self.rentals:
            rental_label = f"{rental['item_name']} ({rental['start_date']} - {rental['end_date']})"
            self.rentals_combobox.addItem(rental_label)
        layout.addWidget(self.rentals_combobox)

        # Добавляем календарь для выбора новой даты окончания аренды
        self.calendar = QCalendarWidget(self)
        self.calendar.setSelectionMode(QCalendarWidget.SelectionMode.SingleSelection)
        layout.addWidget(QLabel("Выберите дату окончания аренды:"))
        layout.addWidget(self.calendar)



        # Кнопка продления аренды
        extend_button = QPushButton("Продлить аренду")
        extend_button.clicked.connect(self.extend_rental)
        layout.addWidget(extend_button)

        # Кнопка отмены аренды
        cancel_button = QPushButton("Отменить аренду")
        cancel_button.clicked.connect(self.cancel_rental)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def load_rentals(self):
        if os.path.exists(RENTAL_DATA_FILE):
            with open(RENTAL_DATA_FILE, "r") as file:
                return [json.loads(line) for line in file.readlines()]
        return []

    def extend_rental(self):
        selected_rental = self.rentals_combobox.currentText()
        if selected_rental == "Выберите аренду":
            QMessageBox.warning(self, "Ошибка", "Выберите аренду для продления.")
            return

        # Логика продления аренды (например, увеличение даты окончания)
        rental = self.get_selected_rental(selected_rental)

        if not rental:  # Если аренда не найдена
            QMessageBox.warning(self, "Ошибка", "Ошибка при нахождении аренды.")
            return
        # Получаем выбранную пользователем дату из календаря
        new_end_date = self.calendar.selectedDate()

        if new_end_date.isNull():
            QMessageBox.warning(self, "Ошибка", "Выберите дату окончания аренды.")
            return

        rental['end_date'] = new_end_date.toString("yyyy-MM-dd")

        self.save_rentals()

        QMessageBox.information(self, "Успех",
                                f"Аренда {rental['item_name']} продлена до {new_end_date.toString('yyyy-MM-dd')}!")

    def cancel_rental(self):
        selected_rental = self.rentals_combobox.currentText()

        if selected_rental == "Выберите аренду":
            QMessageBox.warning(self, "Ошибка", "Выберите аренду для отмены.")
            return

        # Логика отмены аренды
        rental = self.get_selected_rental(selected_rental)
        self.rentals.remove(rental)
        self.save_rentals()

        QMessageBox.information(self, "Успех", f"Аренда {rental['item_name']} отменена!")

    def get_selected_rental(self, rental_label):
        # Ищем аренду по метке (например, по имени товара и датам)
        for rental in self.rentals:
            rental_label_check = f"{rental['item_name']} ({rental['start_date']} - {rental['end_date']})"
            if rental_label == rental_label_check:
                return rental
        return None

    def save_rentals(self):
        with open(RENTAL_DATA_FILE, "w") as file:
            for rental in self.rentals:
                json.dump(rental, file)
                file.write('\n')
                ###

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())