from django.db import models

# Create your models here.


class Student(models.Model):
    name = models.CharField(verbose_name='Имя пользователя', max_length=50)
    surname = models.CharField(verbose_name='Фамилия пользователя', max_length=50)
    email = models.EmailField()
    password = models.CharField(verbose_name='Пароль', max_length=250)

    def __str__(self):
        return self.name + ' ' + self.surname

    def get_full_name(self):
        return self.name + ' ' + self.surname


class Course(models.Model):
    name = models.CharField(verbose_name='Название дисциплины', max_length=50)

    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.name


class HomeworkType(models.Model):
    name = models.CharField(verbose_name='Тема', max_length=50)
    task = models.TextField(default='Дз', verbose_name='Задание')
    deadline = models.DateTimeField(verbose_name='Срок сдачи')

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class HwDone(models.Model):
    text = models.CharField(blank=True, verbose_name='Содержание', max_length=50)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Студент')
    mark = models.IntegerField(blank=False, verbose_name='Оценка')

    hw_type = models.ForeignKey(HomeworkType, on_delete=models.CASCADE)
