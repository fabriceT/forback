from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
'''

from ansible.plugins.callback import CallbackBase
from ansible.module_utils._text import to_bytes, to_text
from ansible.utils.display import Display
from ansible import constants as C
import os


display = Display()

class CallbackModule(CallbackBase):

    '''
    This is the default callback interface, which simply prints messages
    to stdout when new callback events are received.
    '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'awesome'
    CALLBACK_NAME = 'forvia'

    playbook_hosts = {}

    def __init__(self):
        # make sure the expected objects are present, calling the base's __init__
        super(CallbackModule, self).__init__()

    def forwrite(self, result):

        buf = to_bytes(self._dump_results(result._result))

        try:
            path = self.playbook_hosts[result._host.get_name()]
            with open(path, 'ab+') as fd:
                fd.write(to_bytes("\n************ %s *********\n" % result._task.get_name()))
                fd.write(buf)

            display.display("**** " + path + " *****")

        except (OSError, IOError) as e:
            self._display.warning(u"Unable to write to %s's file: %s" % (path, to_text(e)))

    hostname_file = {}

    def v2_runner_item_on_ok(self, result):
        display.display("ok for host: " + result._host.get_name())

    def v2_runner_on_start(self, host, task):
        current_host = host.get_name()
        if current_host not in self.playbook_hosts:
            path = current_host

            display.v("New hosts, new file: %s" % path)
            self.playbook_hosts[current_host] = path

            # TODO: check for exception
            if os.path.exists(path):
                os.remove(path)


        #display.debug("host: " + host + " , task: " + task)
        #display.v(host.get_name())
        #display.v(task.get_name())
        pass

    # Fin d'une tâche
    def v2_runner_on_ok(self, result):
        display.v("*********** v2_runner_on_ok")
        self.forwrite(result)

    def playbook_on_stats(self, stats):
        display.v("*********** playbook_on_stats")
        for k in self.playbook_hosts.keys():
            a = stats.summarize(k)
            display.v("[%s] ok: %d" % (k, a.get("ok")))
