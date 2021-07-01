from django import template
from django.urls import reverse_lazy

from dms.models import Protocol

register = template.Library()


@register.simple_tag
def get_protocol(obj):
    try:
        protocol = Protocol.objects.get(
            object_type=obj.__class__.__name__,
            object=obj.pk
        )
    except Protocol.DoesNotExist:
        protocol = None
    if protocol:
        return protocol.protocol
    else:
        url = reverse_lazy('dms:add-protocol',
                           kwargs={"object_type": obj.__class__.__name__,
                                   "object_id": obj.pk})
        return {
            'url_link': url
        }
