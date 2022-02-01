
def try_remove(iterable, value):
    try:
        iterable.remove(value)
    except ValueError:
        pass
