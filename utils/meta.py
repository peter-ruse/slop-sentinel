import threading


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # Use locks at the class level instead of the
        # metaclass level in order to prevent deadlocks...
        if not hasattr(cls, "_lock"):
            cls._lock = threading.Lock()

        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
