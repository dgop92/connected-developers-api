from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=160)


class Dev(models.Model):
    username = models.CharField(max_length=80)
    organizations = models.ManyToManyField(Organization)


class DevRegister(models.Model):

    dev1 = models.ForeignKey(
        Dev, on_delete=models.CASCADE, related_name="registers_as_dev1"
    )
    dev2 = models.ForeignKey(
        Dev, on_delete=models.CASCADE, related_name="registers_as_dev2"
    )
    connected = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)
    organizations = models.ManyToManyField(Organization)

    class Meta:
        ordering = ["registered_at"]
