import validators


def validator(url):
    return validators.url(url)
