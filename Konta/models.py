from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, newsletter, password=None):
        if not email:
            raise ValueError('Wprowadź poprawny adres email')

        user = self.model(
            email=self.normalize_email(email),
            name=name.capitalize(),
            newsletter=newsletter,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
            newsletter=False,
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Uzytkownik(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True, verbose_name='email')
    name = models.CharField(max_length=30, verbose_name='imię')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='nazwisko')
    phone = models.CharField(max_length=15, blank=True, verbose_name='telefon')
    newsletter = models.BooleanField(default=False)

    last_login = models.DateTimeField(auto_now_add=True, verbose_name='ostatnie logowanie')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='data dołączenia')
    is_active = models.BooleanField(default=False, verbose_name='aktywny')
    is_admin = models.BooleanField(default=False, verbose_name='admin')
    is_superuser = models.BooleanField(default=False, verbose_name='superuser')
    is_staff = models.BooleanField(default=False, verbose_name='staff')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = MyUserManager()

    class Meta:
        verbose_name_plural = 'Użytkownicy'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class Adres(models.Model):
    user = models.ForeignKey(Uzytkownik, null=True, on_delete=models.CASCADE, verbose_name='Użytkownik')
    street_and_house_nr = models.CharField(max_length=50, verbose_name='Ulica i nr domu')
    zipcode = models.CharField(max_length=15, verbose_name='Kod pocztowy')
    city = models.CharField(max_length=50, verbose_name='Miasto')
    country = models.CharField(max_length=50, verbose_name='Kraj')
    company_name = models.CharField(max_length=100, blank=True, verbose_name='Nazwa firmy')
    nip = models.CharField(max_length=15, blank=True, verbose_name='NIP')

    class Meta:
        verbose_name_plural = 'Adresy'

    def __str__(self):
        return f'{self.street_and_house_nr}, {self.zipcode}, {self.city}, {self.country}'
