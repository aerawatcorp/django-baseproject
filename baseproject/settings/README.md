# The settings/ path structure
- This is a README file to explain the things inside this package
- base.py for the base settings to be imported by all environment specific setting files
- env_local.py for local environment (use it for development)
- env_prod.py for production deployment
- env_test.py for test enviroment

There is no specific naming convention, but prod, dev, test, etc would be easier choices

- env_sample.example (a sample file to start with)

PS : Each local settings file should start with importing the base settings `(from .base import *)`

# settings/local.py
This is the default entry point for manage.py, asgi.py and wsgi.py
Sample file - settings/local.example

- This file should basically contain the following line only
```
from .env_dev import * # or anything specific to the environment
```

