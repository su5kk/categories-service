# Введение

Нам нужно разработать систему учета студентов для общеобразовательной школы.

# Решение

## API

### GET /grades
Как работает: возвращает все оценки всех студентов
Клиенту нужно: имена студентов, имена предметов, их класс, оценки

в коде:
1. TODO

### DB schema

Table student(id, name, level)
Table subject(id, name, level)
Table grade(id, student_id, subject_id, date, value)

