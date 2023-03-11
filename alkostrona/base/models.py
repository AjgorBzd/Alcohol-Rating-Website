from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Alcohol(models.Model):
    ALCOHOL_TYPES = (
        ('Vdk', 'Vodka'),
        ('Ber', 'Beer'),
        ('RdW', 'Red Wine'),
        ('WhW', 'White Wine'),
        ('RsW', 'Rose Wine'),
        ('SpW', 'Sparkling Wine'),
        ('Whs', 'Whiskey'),
        ('Lqr', 'Liquor'),
        ('Brb', 'Bourbon'),
        ('Brd', 'Brandy'),
        ('Mns', 'Moonshine'),
        ('Oth', 'Other'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='author')
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=3, choices=ALCOHOL_TYPES)
    volume_l = models.DecimalField(default=1, max_digits=4, decimal_places=2, validators=[
        MinValueValidator(0)
    ])
    percentage = models.FloatField(default=30, validators=[
                                         MinValueValidator(0),
                                         MaxValueValidator(100)
                                     ])
    description = models.TextField(null=True, blank=True)
    alcohol_picture = models.ImageField(default='alcohol_pics/default_alcohol.jpg', upload_to='alcohol_pics')
    likes = models.ManyToManyField(User, default=None, blank=True, related_name='likes')
    reviews = models.ManyToManyField(User, default=None, blank=True, related_name='reviews')
    verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        choice = self.type
        if not any(choice in _tuple for _tuple in self.ALCOHOL_TYPES):
            raise ValueError('You need to choose a type of alcohol.')
        super(Alcohol, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def likes_no(self):
        return self.likes.all().count()


class Like(models.Model):
    LIKE_OPTIONS = (
        ('Like', 'Like'),
        ('Dislike', 'Dislike')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alcohol = models.ForeignKey(Alcohol, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_OPTIONS, default='Like', max_length=10)

    def __str__(self):
        return str(self.alcohol)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, default='')
    profile_picture = models.ImageField(default='profile_pics/default_user.png', upload_to='profile_pics')
    desc = models.TextField(default="A default description")

    def __str__(self):
        return f'{self.user.username}s profile'

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.user.username
        super().save(*args, **kwargs)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alcohol = models.ForeignKey(Alcohol, on_delete=models.CASCADE)
    comment = models.TextField(max_length=3000)
    rate = models.IntegerField(default=0, validators=[
                                         MinValueValidator(0),
                                         MaxValueValidator(5)
                                     ])

    def __str__(self):
        return str(self.alcohol)
