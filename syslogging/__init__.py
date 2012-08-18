# Copyright (c) 2012, Christian Kampka
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import syslog
from logging import Handler

class SyslogHandler(Handler):
    """
    A handler class which opens a connection to the system logger using syslog(3).
    """

    # see syslog(3) for supported syslog priorities
    # not all priorities are supported through standard logging,
    # but might by useful for custom log levels
    levelMap = {
        "ALERT":    syslog.LOG_ALERT,
        "CRIT":     syslog.LOG_CRIT,
        "CRITICAL": syslog.LOG_CRIT,
        "DEBUG":    syslog.LOG_DEBUG,
        "EMERG":    syslog.LOG_EMERG,
        "ERR":      syslog.LOG_ERR,
        "ERROR":    syslog.LOG_ERR,
        "INFO":     syslog.LOG_INFO,
        "NOTICE":   syslog.LOG_NOTICE,
        "PANIC":    syslog.LOG_EMERG,
        "WARN":     syslog.LOG_WARNING,
        "WARNING":  syslog.LOG_WARNING,
    }

    DEFAULT_FACILITY = syslog.LOG_USER

    openlog = syslog.openlog
    syslog = syslog.syslog

    def __init__(self, prefix, options=0, facility=None):
        super(SyslogHandler, self).__init__()

        self.prefix = prefix
        self.options = options
        self.facility = facility or self.DEFAULT_FACILITY

        self.openlog(self.prefix, self.options, self.facility)

    def getPriority(self, levelname):
        """
        Translates logging priorities into their syslog equivalent.
        """
        level = self.levelMap.get(levelname, syslog.LOG_INFO)
        priority = level | self.facility
        return priority

    def emit(self, record):
        """
        Format the message and send it to syslog.
        """
        priority = self.getPriority(record.levelname)

        for line in record.getMessage().split('\n'):
            line = line.strip()
            if line:
                self.syslog(priority, line)
