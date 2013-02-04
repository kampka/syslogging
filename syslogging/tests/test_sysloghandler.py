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

from testtools import TestCase
from fixtures import MonkeyPatch
from fixtures import FakeLogger

import logging
import syslog
from syslogging import SyslogHandler

class FakeSysloggerFixture(FakeLogger):

    def __init__(self, name="", level=logging.INFO, log_format=None, nuke_handlers=True,
                    syslog_prefix="Twisted", syslog_options=0,
                    syslog_facility=SyslogHandler.DEFAULT_FACILITY):
        super(FakeSysloggerFixture, self).__init__(name, level, log_format, nuke_handlers)

        self.prefix = syslog_prefix
        self.options = syslog_options
        self.facility = syslog_facility

        self.opened = None
        self.events = None

        self.logger = None

    def setUp(self):
        super(FakeSysloggerFixture, self).setUp()

        self.useFixture(MonkeyPatch('syslogging.SyslogHandler.openlog', self.openlog))
        self.useFixture(MonkeyPatch('syslogging.SyslogHandler.syslog', self.syslog))

        self.logger = logging.getLogger(self._name)
        syslogHandler = SyslogHandler(self.prefix, self.options, self.facility)
        try:
            self.logger.addHandler(syslogHandler)
        finally:
            self.addCleanup(self.logger.removeHandler, syslogHandler)

    def openlog(self, prefix, options, facility):
        self.opened = (prefix, options, facility)
        self.events = []

    def syslog(self, priority, message):
        self.events.append((priority, message))


class SyslogHandlerTestCase (TestCase):


    def setUp(self):
        super(SyslogHandlerTestCase, self).setUp()

        self.log = self.useFixture(FakeSysloggerFixture())

    def test_emptyMessage(self):

        self.log.logger.info('')
        self.assertEqual(self.log.events, [])

    def test_customPriority(self):
        log = self.useFixture(FakeSysloggerFixture(level=logging.DEBUG))
        log.logger.debug('hello, world')
        self.assertEqual(
            log.events,
            [(syslog.LOG_DEBUG|log.facility, 'hello, world')])

    def test_customFacility(self):

        log = self.useFixture(FakeSysloggerFixture(syslog_facility=syslog.LOG_CRON))
        log.logger.info('hello, world')
        self.assertEqual(
            log.events,
            [(syslog.LOG_INFO|syslog.LOG_CRON, 'hello, world')])

    def test_multilineMessage(self):

        log = self.useFixture(FakeSysloggerFixture())
        log.logger.info("hello,\nworld")
        self.assertEqual(
            log.events,
            [(syslog.LOG_INFO|log.facility, "hello,"),
             (syslog.LOG_INFO|log.facility, "world")])

    def test_multilinetStripsTrailingEmptyLines(self):
        log = self.useFixture(FakeSysloggerFixture())
        log.logger.info("hello,\nworld\n\n")
        self.assertEqual(
            log.events,
            [(syslog.LOG_INFO|log.facility, "hello,"),
             (syslog.LOG_INFO|log.facility, "world")])
