"""Tables definitions"""

import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from netbox_docker import models


class HostTable(NetBoxTable):
    """Host Table definition class"""

    name = tables.Column(linkify=True)
    image_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_docker:image_list",
        url_params={"host_id": "pk"},
        verbose_name="Images count",
    )
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = models.Host
        fields = ("pk", "id", "name", "endpoint", "image_count", "tags")
        default_columns = ("name", "endpoint", "image_count")


class ImageTable(NetBoxTable):
    """Image Table definition class"""

    host = tables.Column(linkify=True)
    name = tables.Column(linkify=True)
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = models.Image
        fields = ("pk", "id", "host", "name", "version", "provider", "size", "tags")
        default_columns = ("name", "version", "provider", "size", "host")
