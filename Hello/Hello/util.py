from functools import wraps

from Hello.models import ImageRequestEvent


def record_access(func):
    @wraps(func)
    def f(*args, **kwargs):
        request = args[0]
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip is None: ip = request.META.get('REMOTE_ADDR')
        path = request.path
        event = ImageRequestEvent(path=path, ip_string=ip)
        event.save()
        print(event)
        return func(*args, **kwargs)
    return f

