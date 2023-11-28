
class SlackNotifier:

    def __init__(self):
        # Set a webhok via an env var, ask Mike for a 
        #web hook url.
        ...

    def notify(self, msg: str):
        # Check formatting options for messages to slack.
        # From memory you style it via sending a dictionary.
        # It's a post request so do use the http client
        # we've developing elsewhere in this library.
        ...