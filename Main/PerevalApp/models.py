from django.db import models


COMPLEXITY = (
    ('', ''),
    ('1А', '1-А'),
    ('2А', '2-А'),
    ('3А', '3-А'),
    ('1Б', '1-Б'),
    ('2Б', '2-Б'),
    ('3Б', '3-Б'),
)

STATUS = (
        ("new", 'новый'),
        ("pending", 'в обработке'),
        ("accepted", 'принят'),
        ("rejected", 'отклонен'),
    )

class Users(models.Model):

    email = models.EmailField(max_length=100)
    fam = models.CharField(max_length=100, verbose_name='Фамилия')
    name = models.CharField(max_length=100, verbose_name='Имя')
    otc = models.CharField(max_length=100, verbose_name='Отчество')
    phone = models.CharField(max_length=11)


class Coords(models.Model):

    latitude = models.FloatField(max_length=20)
    longitude = models.FloatField(max_length=20)
    height = models.IntegerField()


class Levels(models.Model):

    spring = models.CharField(max_length=2, null=True, blank=True, choices=COMPLEXITY)
    summer = models.CharField(max_length=2, null=True, blank=True, choices=COMPLEXITY)
    autumn = models.CharField(max_length=2, null=True, blank=True, choices=COMPLEXITY)
    winter = models.CharField(max_length=2, null=True, blank=True, choices=COMPLEXITY)


class Pereval(models.Model):

    title = models.CharField(max_length=255)
    beauty_title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.TextField(null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE)
    level = models.ForeignKey(Levels, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS, blank=True, default='new')


class Images(models.Model):

    title = models.CharField(max_length=255)
    data = models.ImageField(upload_to='images/')
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images')

