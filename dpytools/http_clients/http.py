# Import and use backoff
# https://pypi.org/project/backoff/


class HttpClient:

    # Methods should use backoff
    # Methods should lof what they are trying to do before they do it.
    # When you backoff and retry it should log each failure and why,
    # as well as which attempt number it is.

    def get(): ...

    def post(): ...
