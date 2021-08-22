from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, ValidationError
from django.db import models
from django.urls import reverse
from datetime import datetime
from django.conf import settings
import pytz
import django_filters
from PIL import Image


utc = pytz.UTC


class Company(models.Model):
    """
    Класс Company представляет информацию о компаниях на сайте.
    """
    title = models.CharField(max_length=100, help_text='―――――', unique=True,
                             verbose_name='Название компании')
    leader_name = models.CharField(max_length=100, help_text='―ФИО', verbose_name='Директор')
    created_date = models.DateTimeField(auto_now_add=True,)
    updated_date = models.DateTimeField(auto_now=True,)
    description = RichTextField(max_length=1000, null=True, help_text='―――――', verbose_name='Краткое описание')
    address = models.CharField(max_length=100, help_text='―――――', verbose_name='Адрес компании')

    class Meta:
        """
        Класс содержит ordering по title.
        """
        ordering = ['title']

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def get_absolute_url(self):
        """
        :return: возвращает url - company-detail
        """
        return reverse('company-detail', args=[str(self.id)])


class Phone(models.Model):
    """
    Класс Phone представляет информацию о телефонах компаний на сайте.
    """
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    phone_regex = RegexValidator(regex=r'^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$')
    phone_number = models.CharField(validators=[phone_regex],
                                    max_length=17, blank=True,
                                    help_text='―пример +380XXXXXXXXX',
                                    verbose_name='Телефон')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.phone_number

    class Meta:
        """
        Класс содержит ordering по company.
        """
        ordering = ['company']


class Email(models.Model):
    """
    Класс Email представляет информацию о e-mails компаний на сайте.
    """
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    email_address = models.EmailField(help_text='―――――', blank=False, verbose_name='E-mail')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.email_address

    class Meta:
        """
        Класс содержит ordering по company.
        """
        ordering = ['company']


class Manager(models.Model):
    """
    Класс Manager представляет информацию о контактных лицах компаний на сайте.
    """
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    manager_name = models.CharField(max_length=100, help_text='―ФИО', blank=False, verbose_name='Контактное лицо')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.manager_name

    class Meta:
        """
        Класс содержит ordering по company.
        """
        ordering = ['company']


class User(AbstractUser):
    """
    Класс User представляет информацию о пользователях сайта.
    """
    photo = models.ImageField(default='default1.jpg', null=True, blank=True, help_text='―――――')
    is_manager = models.BooleanField(default=False, verbose_name='Менеджер')
    is_customer = models.BooleanField(default=False, verbose_name='Заказчик')
    is_admin = models.BooleanField(default=False, verbose_name='Админ')
    phone_regex = RegexValidator(regex=r'^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$')
    phone_number = models.CharField(validators=[phone_regex],
                                    max_length=17, blank=False,
                                    help_text='―пример +380XXXXXXXXX',
                                    verbose_name='Телефон')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.username

    def get_absolute_url(self):
        """
        :return: возвращает url - manager_crm_detail
        """
        return reverse('manager_crm_detail', args=[str(self.id)])


class Customer(models.Model):
    """
    Класс Customer представляет информацию о заказчиках сайта.
    """
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                 verbose_name='Имя пользователя', help_text='―――――')
    name = models.CharField(max_length=100, null=True, blank=False, default='Заказчик',
                            verbose_name='Имя Фамилия (подтвердите)')
    gender_type = [('мужчина', 'мужчина'),
                     ('женщина', 'женщина')]
    gender = models.CharField(max_length=100, choices=gender_type, verbose_name='Пол',
                              blank=True, help_text='―――――')

    def clean(self):
        """
        :return: Если имя и фамиилия заказчика в классе Customer не соотвествует имени и фамилии
        заказчика в классе User - возбуждается ошибка, до того момента пока пользователь не впишет
        имена правильно.
        """
        if self.name != self.user.first_name + " " + self.user.last_name:
            raise ValidationError('Имя Фамилия не совпадают с изменёнными данными, '
                                  'пожалуйста внесите соответствующие изменения')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


class ManagerCRM(models.Model):
    """
    Класс ManagerCRM представляет информацию о менеджерах-CRM сайта.
    """
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                             verbose_name='Имя пользователя', help_text='―――――')
    name = models.CharField(max_length=100, null=True, blank=False, default='Менеджер',
                            verbose_name='Имя Фамилия (подтвердите)')
    gender_type = [('мужчина', 'мужчина'),
                     ('женщина', 'женщина')]
    gender = models.CharField(max_length=100, choices=gender_type, verbose_name='Пол',
                              blank=True, help_text='―――――')

    def clean(self):
        """
        :return: Если имя и фамиилия заказчика в классе ManagerCRM не соотвествует имени и фамилии
        заказчика в классе User - возбуждается ошибка, до того момента пока пользователь не впишет
        имена правильно.
        """
        if self.name != self.user.first_name + " " + self.user.last_name:
            raise ValidationError('Имя Фамилия не совпадают с изменёнными данными, '
                                  'пожалуйста внесите соответствующие изменения')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


def start_date_valid(value):
    """
    Функция для проверки валидности дат начала проекта и окончания проекта в модели Project.
    (на данный момент функция не испульзуется, найдет аналог внутри класса модели, не могу ее удалить
    или закоментировать , так как без нее не проходят миграции..... нформация об этой функции где-то засела в старых
    миграциях и я решил ее оставить, но она не на что не влияит , так как не работает.)
    :param value:
    :return:
    """
    today = datetime.now()
    today = pytz.utc.localize(today)
    if value < today:
        raise ValidationError(('дата начала проекта не может '
                               'быть раньше сегодняшнего дня'))


class Project(models.Model):
    """
    Класс Project представляет информацию о проектах компаний на сайте.
    """
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True,
                                verbose_name='Название компании',
                                help_text='―――――')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True,
                                 verbose_name='Заказчик проекта', help_text='―――――')
    name = models.CharField(max_length=100, unique=True,
                            help_text='―――――', verbose_name='Название проекта',)
    description = RichTextField(max_length=1000, null=True,
                                help_text='―――――',
                                verbose_name='Краткое описание')
    start_date = models.DateTimeField(verbose_name='Дата начала проекта', help_text='― дд.мм.гггг.')
    end_date = models.DateTimeField(verbose_name='Дата окончания проекта', help_text='― дд.мм.гггг.')
    price = models.IntegerField(verbose_name='Стоимость проекта', help_text='― в долларах США')
    status_pro = models.CharField(max_length=100, default='Еще не начат',
                                  verbose_name='Статус проекта', help_text='―――――')

    class Meta:
        """
        Класс содержит ordering.
        """
        ordering = ['name', '-name', 'company', 'price', 'start_date', 'end_date', 'status_pro']
        pass

    def clean(self):
        """
        Функция для проверки валидности дат начала проекта и окончания проекта в модели Project
        :return: Возбуждает ошибку если дата начала проекта старше даты окончания проекта.
        """
        if self.end_date <= self.start_date:
            raise ValidationError("Дата окончания проекта не может быть "
                                  "раньше даты начала проекта")

    def get_absolute_url(self):
        """
        :return: возвращает url - project-detail
        """
        return reverse('project-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        """
        Функция для определения статуса проекта по датам начала и окончания проекта.
        """
        today = datetime.now()
        today = pytz.utc.localize(today)
        if self.start_date > today:
            self.status_pro = 'Еще не начат'
        elif self.start_date <= today <= self.end_date:
            self.status_pro = 'В процессе разработки'
        elif self.end_date < today:
            self.status_pro = 'Выполнен'
        return super().save(*args, **kwargs)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


class Interaction(models.Model):
    """
    Класс Interaction представляет информацию о взаимодействиях по проектам компаний на сайте.
    """
    channels = [('Телефонный звонок', 'Телефонный звонок'),
                ('Переписка по E-mail', 'Переписка по E-mail'),
                ('Переписка в мессенджере', 'Переписка в мессенджере')]

    rating_com = [('☆', '☆'),
                  ('☆☆', '☆☆'),
                  ('☆☆☆', '☆☆☆'),
                  ('☆☆☆☆', '☆☆☆☆'),
                  ('☆☆☆☆☆', '☆☆☆☆☆')]

    reference_obj_list = [('с компанией', 'с компанией'), ('с заказчиком', 'с заказчиком')]

    channel_of_reference = models.CharField(max_length=100, choices=channels,
                                            verbose_name='Канал связи', help_text='―――――')
    reference_obj = models.CharField(max_length=100, null=True, choices=reference_obj_list,
                                     verbose_name='Вид связи', help_text='―――――')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True,
                                verbose_name='Название проекта',
                                help_text='―――――')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True,
                                verbose_name='Компания', default=None, blank=True, help_text='―――――')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True,
                                 verbose_name='Заказчик проекта', default=None, blank=True, help_text='―――――')
    created_date = models.DateTimeField(auto_now_add=True,)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                null=True,
                                verbose_name='Менеджер',
                                help_text='―――――')
    description = RichTextField(max_length=1000, null=True,
                                help_text='―――――',
                                verbose_name='Описание')
    rating = models.CharField(max_length=100, choices=rating_com, verbose_name='Оценка', help_text='―――――')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.channel_of_reference

    def save(self, *args, **kwargs):
        """
        Функция возвращает None для поля company если пользователь выбрал вид связи 'с заказчиком'.
        Функция возвращает None для поля customer если пользователь выбрал вид связи 'с компанией'.
        """
        if self.reference_obj == 'с заказчиком':
            self.company = None
        if self.reference_obj == 'с компанией':
            self.customer = None
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        :return: возвращает url - interaction-detail
        """
        return reverse('interaction-detail', args=[str(self.id)])

