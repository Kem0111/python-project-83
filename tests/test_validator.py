from page_analyzer.validate import validator


def test_validator():
    assert validator('https://ru.hexlet.io/programs')
    assert not validator('https://ru.hexlet.')
