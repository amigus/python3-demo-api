#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import create_app

application = create_app()

if __name__ == "__main__":
    application.run()
