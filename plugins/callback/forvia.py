from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
'''

from ansible.plugins.callback import CallbackBase
from ansible.module_utils._text import to_bytes, to_text
from ansible.utils.display import Display
from ansible import constants as C


display = Display()

class CallbackModule(CallbackBase):

    '''
    This is the default callback interface, which simply prints messages
    to stdout when new callback events are received.
    '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'awesome'
    CALLBACK_NAME = 'forvia'

    def __init__(self):
        # make sure the expected objects are present, calling the base's __init__
        super(CallbackModule, self).__init__()

    def forwrite(self, result):

        buf = to_bytes(self._dump_results(result._result))

        try:
            path = result._host.get_name()
            with open(path, 'wb+') as fd:
                fd.write(buf)

            display.display("**** " + path + " *****")

        except (OSError, IOError) as e:
            self._display.warning(u"Unable to write to %s's file: %s" % (path, to_text(e)))

    hostname_file = {}

    def v2_runner_item_on_ok(self, result):
        display.display("ok for host: " + result._host.get_name())
        pass

    def v2_runner_on_start(self, host, task):
        #display.debug("host: " + host + " , task: " + task)
        display.v(host.get_name())
        display.v(task.get_name())
        pass

    # Fin d'une tâche
    def v2_runner_on_ok(self, result):
        display.v("v2_runner_on_ok")
        self.forwrite(result)
        pass

