from django.db import models
from django.db.models import CASCADE

class technique(models.Model):
    name = models.CharField('Наименование', max_length=100)
    type = models.CharField('Тип техники', max_length=100)
    amount = models.CharField('Количество', max_length=100)
    inventory_number = models.CharField('Инвентарный номер', max_length=100)
    manufacture_number = models.CharField('Заводской номер', max_length=100)
    residual_value = models.IntegerField('Остаточная стоимость')
    date_of_manufacture = models.DateField('Дата производства')
    date_of_purchase = models.DateField('Дата покупки')
    contract_number = models.CharField('Номер договора', max_length=100)
    country_of_manufacture = models.CharField('Страна производства', max_length=100)

    def __str__(self):
        return self.name
class directory(models.Model):
    directory_name = models.CharField('Наименование', max_length=100)
class countries_directory(models.Model):
    dir = models.ForeignKey(directory, on_delete=CASCADE)
    country_name = models.CharField('Название страны', max_length=100)
    country_code = models.IntegerField('Код страны')
class types_directory(models.Model):
    dir = models.ForeignKey(directory, on_delete=CASCADE)
    type_name = models.CharField('Название типа техники', max_length=100)








