import sys
import json
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QTextEdit, QHBoxLayout, QCheckBox, QPushButton,
                             QComboBox, QListWidget, QListWidgetItem, QMessageBox, QInputDialog)
from PyQt6.QtCore import Qt

TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tasks = []

        self.counter_label = QLabel("Created tasks: 0")
        self.setWindowTitle("To-Do List")
        self.resize(450, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.vbox = QVBoxLayout()
        central_widget.setLayout(self.vbox)

        self.label_task = QLabel("Task")
        self.line_edit_task = QLineEdit()
        self.char_cnt_label = QLabel("Название: 0 символов")

        self.label_description = QLabel("Description")
        self.line_edit_description = QTextEdit()
        self.line_edit_description.setFixedHeight(60)

        self.priority_layout = QHBoxLayout()
        self.priority_layout.addWidget(QLabel("Priority:"))
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])
        self.priority_combo.setCurrentText("Medium")
        self.priority_layout.addWidget(self.priority_combo)

        self.checkbox_layout = QHBoxLayout()
        self.check_box_1 = QCheckBox("Important")
        self.check_box_2 = QCheckBox("Send notification")
        self.checkbox_layout.addWidget(self.check_box_1)
        self.checkbox_layout.addWidget(self.check_box_2)

        self.button_layout = QHBoxLayout()
        self.button_create = QPushButton("Create task")
        self.button_remove = QPushButton("Delete last")
        self.button_clear = QPushButton("Clear form")
        self.button_clear_list = QPushButton("Clear list")
        self.button_about = QPushButton("About")
        self.button_edit = QPushButton("Edit task")

        self.button_layout.addWidget(self.button_create)
        self.button_layout.addWidget(self.button_remove)
        self.button_layout.addWidget(self.button_clear)
        self.button_layout.addWidget(self.button_clear_list)
        self.button_layout.addWidget(self.button_about)
        self.button_layout.addWidget(self.button_edit)

        self.filter_task = QComboBox()
        self.filter_task.addItems(["All", "Low", "Medium", "High"])
        self.status_task = QLabel("status: ready")
        self.task_list = QListWidget()

        self.vbox.addWidget(self.label_task)
        self.vbox.addWidget(self.line_edit_task)
        self.vbox.addWidget(self.char_cnt_label)
        self.vbox.addWidget(self.label_description)
        self.vbox.addWidget(self.line_edit_description)
        self.vbox.addLayout(self.priority_layout)
        self.vbox.addLayout(self.checkbox_layout)
        self.vbox.addLayout(self.button_layout)
        self.vbox.addWidget(self.status_task)
        self.vbox.addWidget(self.filter_task)
        self.vbox.addWidget(self.task_list)
        self.vbox.addWidget(self.counter_label)

        self.filter_task.currentTextChanged.connect(self.update_tasks)
        self.button_create.clicked.connect(self.create_task)
        self.button_remove.clicked.connect(self.delete_task)
        self.button_clear.clicked.connect(self.clear_form)
        self.line_edit_task.textChanged.connect(self.title_changed)
        self.button_clear_list.clicked.connect(self.clear_list)
        self.button_about.clicked.connect(self.show_about)
        self.button_edit.clicked.connect(self.edit_task)

        self.setStyleSheet("""
        QMainWindow { background-color: #4169E1; }
        QLabel { color: white; }
        QPushButton { background-color: #FFFAFA; color: #191970; padding: 6px; }
        QPushButton:hover { background-color: #E0FFFF; }
        QPushButton:disabled { background-color: #A9A9A9; color: #696969; }
        QLineEdit, QTextEdit, QListWidget, QComboBox { background-color: #E0FFFF; color: #191970; }
        """)

        self.load_tasks()

    def create_task(self):
        line = self.line_edit_task.text().strip()
        if not line:
            QMessageBox.warning(self, "Ошибка", "Название задачи не должно быть пустым")
            return

        task_id = max([t["id"] for t in self.tasks], default=0) + 1

        task_data = {
            "id": task_id,
            "task": line,
            "description": self.line_edit_description.toPlainText(),
            "priority": self.priority_combo.currentText(),
            "important": "Yes" if self.check_box_1.isChecked() else "No",
            "send": "Yes" if self.check_box_2.isChecked() else "No",
        }

        self.tasks.append(task_data)
        self.save_tasks()
        self.update_tasks()
        self.clear_form()
        self.status_task.setText("Задача создана")

    def edit_task(self):
        current_item = self.task_list.currentItem()

        if not current_item:
            QMessageBox.warning(self, "Внимание", "Сначала кликните на задачу в списке, чтобы выделить её!")
            return

        task_id = current_item.data(Qt.ItemDataRole.UserRole)

        task_to_edit = None
        for task in self.tasks:
            if task["id"] == task_id:
                task_to_edit = task
                break

        if not task_to_edit:
            return

        new_name, ok = QInputDialog.getText(self, "Редактирование", "Новое название:", text=task_to_edit["task"])

        if ok and new_name.strip():
            task_to_edit["task"] = new_name.strip()

            self.save_tasks()
            self.update_tasks()


            QMessageBox.information(self, "Успех", "Задача успешно изменена и сохранена!")
            self.status_task.setText("Status: Task edited")

    def delete_task(self):
        if not self.tasks:
            return
        self.tasks.pop()
        self.save_tasks()
        self.update_tasks()
        self.status_task.setText("Status: Task deleted")

    def update_tasks(self):
        self.task_list.clear()
        self.button_remove.setEnabled(len(self.tasks) > 0)
        self.button_edit.setEnabled(len(self.tasks) > 0)

        self.counter_label.setText(f"Created tasks: {len(self.tasks)}")

        if not self.tasks:
            self.task_list.addItem("Задач пока нет...")
            self.status_task.setText("Задач: 0")
            return

        curr_task = self.filter_task.currentText()
        filter_tasks = self.tasks if curr_task == "All" else [t for t in self.tasks if t['priority'] == curr_task]

        if not filter_tasks:
            self.status_task.setText("Нет задач с таким приоритетом")
            return

        for i, task in enumerate(filter_tasks, start=1):
            decs = task["description"]
            item_text = f'№{i}. {task["task"]} - {task["priority"]} \nОписание: {decs} \nВажная: {task["important"]}\nУведомление: {task["send"]}'
            item = QListWidgetItem(item_text)

            item.setData(Qt.ItemDataRole.UserRole, task["id"])

            self.task_list.addItem(item)

    def show_about(self):
        QMessageBox.about(self, "О программе", "To-Do List v2.0\n\nВыполнила: студентка ОРИС")

    def clear_form(self):
        self.line_edit_task.clear()
        self.line_edit_description.clear()
        self.priority_combo.setCurrentText("Medium")
        self.check_box_1.setChecked(False)
        self.check_box_2.setChecked(False)

    def clear_list(self):
        if not self.tasks:
            QMessageBox.warning(self, "Внимание", "Список задач и так пуст")
            return

        reply = QMessageBox.question(self, "Подтверждение", "Удалить все задачи?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.tasks.clear()
            self.save_tasks()
            self.update_tasks()
            self.status_task.setText("Status: List cleared")

    def title_changed(self, text):
        self.char_cnt_label.setText(f"Название: {len(text.split())} слов")

    def save_tasks(self):
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump(self.tasks, file, ensure_ascii=False, indent=4)

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r", encoding="utf-8") as file:
                self.tasks = json.load(file)
                self.update_tasks()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())