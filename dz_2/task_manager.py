import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QTextEdit, QRadioButton, QCheckBox, QPushButton, QComboBox,
    QVBoxLayout, QHBoxLayout
)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.resize(520, 720)

        self.tasks = []

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        main_layout.addWidget(QLabel("Task:"))
        self.task_edit = QLineEdit()
        main_layout.addWidget(self.task_edit)

        main_layout.addWidget(QLabel("Description:"))
        self.desc_edit = QTextEdit()
        self.desc_edit.setFixedHeight(80)
        main_layout.addWidget(self.desc_edit)

        main_layout.addWidget(QLabel("Priority:"))
        priority_widget = QWidget()
        priority_layout = QHBoxLayout(priority_widget)
        priority_layout.setContentsMargins(0, 0, 0, 0)

        self.low_rb = QRadioButton("Low")
        self.medium_rb = QRadioButton("Medium")
        self.high_rb = QRadioButton("High")
        self.medium_rb.setChecked(True)

        priority_layout.addWidget(self.low_rb)
        priority_layout.addWidget(self.medium_rb)
        priority_layout.addWidget(self.high_rb)
        main_layout.addWidget(priority_widget)

        main_layout.addWidget(QLabel("Additional:"))
        self.important_check = QCheckBox("Important")
        self.notify_check = QCheckBox("Send notification")
        self.favorite_check = QCheckBox("Add to favorites")
        main_layout.addWidget(self.important_check)
        main_layout.addWidget(self.notify_check)
        main_layout.addWidget(self.favorite_check)

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        self.create_button = QPushButton("Create task")
        self.clear_button = QPushButton("Clear")
        self.delete_last_button = QPushButton("Delete last task")

        self.create_button.clicked.connect(self.on_create_task)
        self.clear_button.clicked.connect(self.on_clear)
        self.delete_last_button.clicked.connect(self.on_delete_last)

        buttons_layout.addWidget(self.create_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addWidget(self.delete_last_button)
        main_layout.addWidget(buttons_widget)

        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        filter_layout.setContentsMargins(0, 0, 0, 0)

        filter_layout.addWidget(QLabel("Filter:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Low", "Medium", "High"])
        self.filter_combo.currentIndexChanged.connect(self.on_filter_changed)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addStretch()
        main_layout.addWidget(filter_widget)

        self.status_label = QLabel("Status: Ready")
        self.counter_label = QLabel("Created tasks: 0")
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.counter_label)

        main_layout.addWidget(QLabel("Result:"))
        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)
        main_layout.addWidget(self.result_edit)

    def get_priority(self):
        if self.low_rb.isChecked():
            return "Low"
        elif self.high_rb.isChecked():
            return "High"
        return "Medium"

    def on_create_task(self):
        name = self.task_edit.text().strip()
        description = self.desc_edit.toPlainText().strip()

        extras = []
        if self.important_check.isChecked():
            extras.append("Important")
        if self.notify_check.isChecked():
            extras.append("Send notification")
        if self.favorite_check.isChecked():
            extras.append("Add to favorites")

        task = {
            "name": name,
            "description": description,
            "priority": self.get_priority(),
            "extras": extras,
        }
        self.tasks.append(task)

        self.status_label.setText("Status: Task created")
        self.counter_label.setText(f"Created tasks: {len(self.tasks)}")
        self.update_result()

    def on_clear(self):
        self.task_edit.clear()
        self.desc_edit.clear()
        self.medium_rb.setChecked(True)
        self.important_check.setChecked(False)
        self.notify_check.setChecked(False)
        self.favorite_check.setChecked(False)
        self.status_label.setText("Status: Ready")

    def on_delete_last(self):
        if self.tasks:
            self.tasks.pop()
            self.counter_label.setText(f"Created tasks: {len(self.tasks)}")
            self.update_result()

    def on_filter_changed(self):
        self.update_result()

    def update_result(self):
        selected_filter = self.filter_combo.currentText()

        lines = []
        for index, task in enumerate(self.tasks, 1):
            if selected_filter != "All" and task["priority"] != selected_filter:
                continue
            extras = ", ".join(task["extras"]) if task["extras"] else "none"
            lines.append(
                f"#{index} {task['name']}\n"
                f"  Priority: {task['priority']}\n"
                f"  Extras: {extras}\n"
                f"  Description: {task['description']}"
            )

        if not lines:
            self.result_edit.setPlainText("No tasks")
        else:
            self.result_edit.setPlainText("\n\n".join(lines))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()