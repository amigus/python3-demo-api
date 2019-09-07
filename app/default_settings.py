# -*- coding: utf-8 -*-
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Use "sub" instead of "identity" to be compliant with OpenID Connect
JWT_IDENTITY_CLAIM = "sub"
# Enable "query_string" for email verification and password reset
JWT_TOKEN_LOCATION = ["headers", "query_string"]
