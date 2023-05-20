from .schemas import Link


def link_serializer(obj: dict) -> Link:
    """
    Parse link data from database into Link model schema.
    """
    return Link.parse_obj(obj)
