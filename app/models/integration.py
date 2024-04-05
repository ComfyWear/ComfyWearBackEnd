from utils.abstract_model import AbstractModel


class Integration(AbstractModel):
    """
    Represents a collection of related data for a particular integration
    within the system.

    This model inherits from the AbstractModel and contains an auto-generated
    UUID as a primary key.

    :return: A string representation of the integration's UUID.
    :rtype: str
    """

    class Meta:
        app_label = "app"
        verbose_name = "Integration"
        verbose_name_plural = "Integrations"
        ordering = ["id"]
