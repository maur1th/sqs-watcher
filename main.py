import subprocess
import boto3


QUEUE_URL = "url"
TRIGGER = "deploy"
COMMAND = ["echo", "toto"]


# https://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration
session = boto3.Session(profile_name="profile")
client = session.client("sqs")


def poll(queue_url, trigger, command):
    """ Check if SQS message present, trigger command
    """
    response = client.receive_message(QueueUrl=queue_url,
                                      WaitTimeSeconds=20,
                                      MaxNumberOfMessages=1)
    message = response.get("Messages", [{}])[0]
    if message.get("Body") != trigger:
        return
    subprocess.run(command)
    client.delete_message(QueueUrl=queue_url,
                          ReceiptHandle=message["ReceiptHandle"])


if __name__ == "__main__":

    while True:
        poll(QUEUE_URL, TRIGGER, COMMAND)
