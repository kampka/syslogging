===========
syslogging
===========
-------------------------------------------------
A syslog(3) LogHandler for pythons logging system
-------------------------------------------------

|travis| |pypi|

.. |pypi| image:: https://badge.fury.io/py/syslogging.svg
    :target: https://badge.fury.io/py/syslogging

.. |travis| image:: https://travis-ci.org/kampka/syslogging.png?branch=master
    :target: https://travis-ci.org/kampka/syslogging

This modules provides a LogHandler for pythons logging system
that logs to the system logger using syslog(3) instead of
talking to the system logger over socket connections directly.

Example::
    >>> import logging
    >>> from syslogging import SyslogHandler
    >>> logger = logging.getLogger("my-application")
    >>> logger.addHandler(SyslogHandler("my-application"))
    >>> logger.error("Hello World")
