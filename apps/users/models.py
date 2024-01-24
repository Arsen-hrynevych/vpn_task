from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from urllib.parse import urlparse


class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    Attributes:
        email (EmailField): Email address of the user.
        groups (ManyToManyField): Groups to which the user belongs.
        user_permissions (ManyToManyField): Permissions assigned directly to the user.
    """
    email = models.EmailField(unique=True, verbose_name='Email Address')
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',
        blank=True,
        verbose_name='Groups',
        help_text=(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'
        ),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_user_permissions',
        blank=True,
        verbose_name='User Permissions',
        help_text='Specific permissions for this user.',
    )

    class Meta:
        app_label = 'users'

    def __str__(self):
        return self.username


class CreatedSite(models.Model):
    """
    Model representing a created site.

    Attributes:
        name (CharField): Name of the site.
        url (URLField): URL of the site.
        user (ForeignKey): User associated with the created site.
    """
    name = models.CharField(max_length=255)
    url = models.URLField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)

    class Meta:
        app_label = 'users'

    def url_path(self):
        """
        Extract and return the path component from the site's URL.
        """
        return urlparse(self.url).path

    def __str__(self):
        return f"{self.name} - {self.url}"


class PageTransitionStatistic(models.Model):
    """
    Model representing statistics for page transitions.

    Attributes:
        site (ForeignKey): Site associated with the statistics.
        site_name (CharField): Name of the site for display purposes.
        transitions_count (PositiveIntegerField): Count of page transitions.
        data_volume_sent (PositiveIntegerField): Total data volume sent.
        data_volume_received (PositiveIntegerField): Total data volume received.
    """
    site = models.ForeignKey(CreatedSite, on_delete=models.CASCADE, null=True, unique=False, related_name='statistics')
    site_name = models.CharField(max_length=255)
    transitions_count = models.PositiveIntegerField(default=0)
    data_volume_sent = models.PositiveIntegerField(default=0)
    data_volume_received = models.PositiveIntegerField(default=0)

    def update_statistics(self, data_sent, data_received):
        """
        Update the statistics with new data.

        Args:
            data_sent (int): Amount of data sent during the transition.
            data_received (int): Amount of data received during the transition.
        """
        self.transitions_count += 1
        self.data_volume_sent += data_sent
        self.data_volume_received += data_received
        self.save()

    class Meta:
        app_label = 'users'

    def __str__(self):
        return (f"{self.site_name} - Transitions: {self.transitions_count}, Sent: {self.data_volume_sent} bytes, "
                f"Received: {self.data_volume_received} bytes")
