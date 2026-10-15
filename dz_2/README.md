
## Команды и элементы интерфейса

**Task** однострочное поле для названия задачи (`QLineEdit`).

**Description** многострочное поле описания (`QTextEdit`).

**Priority** выбор приоритета Low / Medium / High (`QRadioButton`).
  Одновременно может быть выбран только один вариант.

**Additional** дополнительные настройки: Important, Send notification,
  Add to favorites (`QCheckBox`). Можно выбрать любое количество.

**Create task** создать задачу и показать её в поле Result.

**Clear** очистить форму.

**Delete last task** удалить последнюю созданную задачу.

**Filter** фильтр задач по приоритету: All / Low / Medium / High
  (`QComboBox`).

**Status** статус приложения: `Ready` или `Task created`.

**Created tasks** счётчик созданных задач.

**Result** поле для отображения созданных задач.

## Как это работает

1. Пользователь заполняет поля Task, Description, выбирает Priority
   и дополнительные настройки.
2. Нажимает **Create task**.
3. Приложение собирает данные из формы, создаёт задачу и добавляет
   её в общий список задач (Python-список `self.tasks`).
4. Задача отображается в поле Result.
5. Счётчик Created tasks увеличивается на 1, статус меняется на
   `Task created`.
6. Фильтр позволяет показать только задачи с выбранным приоритетом.

## Используемые layout'ы

`QVBoxLayout` главный вертикальный layout окна.

`QHBoxLayout`  для строки приоритетов, строки кнопок и строки фильтра.

Layout'ы вкладываются друг в друга: строки с приоритетами, кнопками
и фильтром собраны в отдельные `QWidget`-контейнеры с горизонтальным
layout'ом, которые затем добавляются в главный вертикальный layout.

## Сигналы и слоты


`self.create_button.clicked.connect(self.on_create_task)`
`self.clear_button.clicked.connect(self.on_clear)`
`self.delete_last_button.clicked.connect(self.on_delete_last)`
`self.filter_combo.currentIndexChanged.connect(self.on_filter_changed)`

Сигнал `clicked` кнопки вызывает метод-слот, который собирает данные
из формы и обновляет результат. Сигнал `currentIndexChanged` у
`QComboBox` перерисовывает список задач при смене фильтра.

## Дополнительный блок

Реализованы все пункты из блока «По желанию»:

кнопка **Clear** очищает форму;

надпись **Status** (`Ready` → `Task created`);

результат отображается внутри окна, а не в консоли;

счётчик **Created tasks: N**;

кнопка **Delete last task**; 

задачи хранятся в Python-списке `self.tasks`;

**QComboBox** для фильтра: All / Low / Medium / High.