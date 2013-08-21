This is a sample starter django application for prismic.

Configuration
-------------
Inside your settings.py, add a dictionary PRISMIC with two keys:

* api - API endpoint
* token - If specified, this token is used for all "guest" requests

Example:

    PRISMIC = {
        "api": "http://your_name.prismic.io/api",
        "token": ""
    }