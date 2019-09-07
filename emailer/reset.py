from .base import Emailer


class Reset(Emailer):
    @staticmethod
    def html(grant):
        return f"""
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title></title>
    </head>
    <body>
        Use the <i>access_token</i> from the OAuth2 grant below, to create an
        HTTP <i>Authorization</i> header:
        <blockquote>
            <code>Authorization: Bearer <i>access_token</i></code>
        </blockquote>
        Then use it to <code>POST {{'password': 'new pass phrase'}}</code> to
            <code>/account/password</code>.</p>
        <blockquote>
            <code>{grant}</code>
        </blockquote>
    </body>
</html>     """

    @staticmethod
    def text(grant):
        return (
            "Use this access_token to POST {'password': 'new pass phrase'}"
            f" to /account/password:\r\n{grant}"
        )

    def __init__(self, sender, subject):
        super().__init__(sender, subject, self.html, self.text)
