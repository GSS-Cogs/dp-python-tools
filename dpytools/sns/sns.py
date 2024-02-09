# See here: https://docs.aws.amazon.com/code-library/latest/ug/python_3_sns_code_examples.html
# Ideally we want to publish a message by passing in a dictionary.
# If SNS doesn not support that stringify any dict that is a message
# when its passed in.

# TODO:
# setup a fake queue using localstack
# https://medium.com/@anchan.ashwithabg95/using-localstack-sns-and-sqs-for-devbox-testing-fa09de5e3bbb
# create a topic of "trial-topic" and work out how to get SNS messages in and out
# of it.

from typing import Union


# Note: return True if it works and False if we hit errors
# (so we can control the flow in calling programs)
def publish(topic: str, msg: Union[str, dict]) -> bool:
    """ """


# For this you'll want boto3 again, create a subscription
# when the class is instantiated (error if you cant)
# The get_message() needs to pull from the queue that's
# been subscribed to.
class Subscription:
    def __init__(self, topic):
        """
        subscrube to a topic (i.e setup to read messages)
        """
        ...

    def get_message(self, wait_time=30):
        """
        Needs to:

        - try and read a message
        - if there's no message, wait until there is a message
          i.e try 30 seconds later

        If the message received is in the form of a dictioary
        (even a stringified one) we want to be returning it
        in the form of a dictionary.
        """
