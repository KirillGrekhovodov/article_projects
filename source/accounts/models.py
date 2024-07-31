from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


from django.contrib.auth import get_user_model


def avatar_path(instance, filename):
    return f'avatars/{instance.user.id}/{filename}'


# def avatar_size_validate(value):
#     print(type(value), "validation")
#     size = value.file.size
#     if size > 3000:
#         raise ValidationError("File too big")


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE, verbose_name='Пользователь')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to=avatar_path,
        verbose_name='Аватар',
        # validators=[avatar_size_validate]
    )

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

