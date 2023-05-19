from .schemas import Link


def link_serializer(obj: dict) -> Link:
    """
    Parse link data from database into Link model schema.
    """
    return Link.parse_obj(obj)


def link_endpoint_serializer(link_obj: Link) -> dict:
    """
    Custom parser Link object into dict.
    """
    obj = link_serializer(link_obj).dict()
    obj.update({'id': str(obj.get('id'))})
    return obj
