from .base import Emailer


class Verify(Emailer):
    @staticmethod
    def html(link):
        return f"""
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title></title>
    </head>
    <body>
        <p>
            Click <a href="{link}">here</a> or paste this link into your browser
            to confirm your email address:<br/>
            {link}
        </p>
    </body>
</html>     """

    @staticmethod
    def text(link):
        return f"Paste this link into your browser to verify your email:\r\n{link}"

    def __init__(self, sender, subject):
        super().__init__(sender, subject, self.html, self.text)
