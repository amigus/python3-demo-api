from abc import ABC, abstractmethod


class Sender(ABC):
    def __init__(self, address, **kwargs):
        self.address = address

    @abstractmethod
    def __call__(self, email, subject, html, text):
        """ send an email with subject from sender containing the html and text """


class Emailer(ABC):
    def __init__(self, email_sender, subject, html_callback, text_callback):
        self.subject = subject
        self.email_sender = email_sender
        self.html_callback = html_callback
        self.text_callback = text_callback

    def __call__(self, email, obj):
        self.email_sender(
            email, self.subject, self.html_callback(obj), self.text_callback(obj)
        )
