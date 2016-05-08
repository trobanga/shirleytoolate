
def trailing_slash(name):
    """
    Add trailing '/' to name if it has none
    """
    if name and name[-1] != '/':
        name += '/'
    return name
