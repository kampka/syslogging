===========
syslogging
===========
-------------------------------------------------
A syslog(3) LogHandler for pythons logging system
-------------------------------------------------

This modules provides a LogHandler for pythons logging system
that logs to the system logger using syslog(3) instead of
talking to the system logger over socket connections directly.

Example::
    >>> import logging
    >>> from syslogging import SyslogHandler
    >>> logger = logging.getLogger("my-application")
    >>> logger.addHandler(SyslogHandler("my-application"))
    >>> logger.error("Hello World")
