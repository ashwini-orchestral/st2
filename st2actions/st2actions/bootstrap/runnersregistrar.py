# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from st2common import log as logging
from st2common.exceptions.db import StackStormDBObjectNotFoundError
from st2common.models.api.action import RunnerTypeAPI
from st2common.persistence.action import RunnerType
from st2common.util.action_db import get_runnertype_by_name
from st2common.constants.runners import LOCAL_RUNNER_DEFAULT_ACTION_TIMEOUT
from st2common.constants.runners import FABRIC_RUNNER_DEFAULT_ACTION_TIMEOUT
from st2common.constants.runners import FABRIC_RUNNER_DEFAULT_REMOTE_DIR
from st2common.constants.runners import PYTHON_RUNNER_DEFAULT_ACTION_TIMEOUT

__all__ = [
    'register_runner_types',
    'RUNNER_TYPES'
]


LOG = logging.getLogger(__name__)

RUNNER_TYPES = [
    {
        'name': 'run-local',
        'description': 'A runner to execute local actions as a fixed user.',
        'enabled': True,
        'runner_parameters': {
            'cmd': {
                'description': 'Arbitrary Linux command to be executed on the '
                               'host.',
                'type': 'string'
            },
            'cwd': {
                'description': 'Working directory where the command will be executed in',
                'type': 'string'
            },
            'env': {
                'description': ('Environment variables which will be available to the command'
                                '(e.g. key1=val1,key2=val2)'),
                'type': 'object'
            },
            'sudo': {
                'description': 'The command will be executed with sudo.',
                'type': 'boolean',
                'default': False
            },
            'kwarg_op': {
                'description': 'Operator to use in front of keyword args i.e. "--" or "-".',
                'type': 'string',
                'default': '--'
            },
            'timeout': {
                'description': ('Action timeout in seconds. Action will get killed if it '
                                'doesn\'t finish in timeout seconds.'),
                'type': 'integer',
                'default': LOCAL_RUNNER_DEFAULT_ACTION_TIMEOUT
            }
        },
        'runner_module': 'st2actions.runners.localrunner'
    },
    {
        'name': 'run-local-script',
        'description': 'A runner to execute local actions as a fixed user.',
        'enabled': True,
        'runner_parameters': {
            'cwd': {
                'description': 'Working directory where the script will be executed in',
                'type': 'string'
            },
            'env': {
                'description': ('Environment variables which will be available to the script'
                                '(e.g. key1=val1,key2=val2)'),
                'type': 'object'
            },
            'sudo': {
                'description': 'The command will be executed with sudo.',
                'type': 'boolean',
                'default': False
            },
            'kwarg_op': {
                'description': 'Operator to use in front of keyword args i.e. "--" or "-".',
                'type': 'string',
                'default': '--'
            },
            'timeout': {
                'description': ('Action timeout in seconds. Action will get killed if it '
                                'doesn\'t finish in timeout seconds.'),
                'type': 'integer',
                'default': LOCAL_RUNNER_DEFAULT_ACTION_TIMEOUT
            }
        },
        'runner_module': 'st2actions.runners.localrunner'
    },
    {
        'name': 'run-remote',
        'description': 'A remote execution runner that executes actions '
                       'as a fixed system user.',
        'enabled': True,
        'runner_parameters': {
            'hosts': {
                'description': 'A comma delimited string of a list of hosts '
                               'where the remote command will be executed.',
                'type': 'string',
                'required': True
            },
            'username': {
                'description': ('Username used to log-in. If not provided, '
                                'default username from config is used.'),
                'type': 'string',
                'required': False
            },
            'password': {
                'description': ('Password used to log in. If not provided, '
                                'private key from the config file is used.'),
                'type': 'string',
                'required': False
            },
            'private_key': {
                'description': ('Private key used to log in. If not provided, '
                                'private key from the config file is used.'),
                'type': 'string',
                'required': False
            },
            'cmd': {
                'description': 'Arbitrary Linux command to be executed on the '
                               'remote host(s).',
                'type': 'string'
            },
            'cwd': {
                'description': 'Working directory where the script will be executed in',
                'type': 'string'
            },
            'env': {
                'description': ('Environment variables which will be available to the command'
                                '(e.g. key1=val1,key2=val2)'),
                'type': 'object'
            },
            'parallel': {
                'description': 'Default to parallel execution.',
                'type': 'boolean',
                'default': True,
                'immutable': True
            },
            'sudo': {
                'description': 'The remote command will be executed with sudo.',
                'type': 'boolean',
                'default': False
            },
            'dir': {
                'description': 'The working directory where the script will be copied to ' +
                               'on the remote host.',
                'type': 'string',
                'default': FABRIC_RUNNER_DEFAULT_REMOTE_DIR,
                'immutable': True
            },
            'kwarg_op': {
                'description': 'Operator to use in front of keyword args i.e. "--" or "-".',
                'type': 'string',
                'default': '--'
            },
            'timeout': {
                'description': ('Action timeout in seconds. Action will get killed if it '
                                'doesn\'t finish in timeout seconds.'),
                'type': 'integer',
                'default': FABRIC_RUNNER_DEFAULT_ACTION_TIMEOUT
            }
        },
        'runner_module': 'st2actions.runners.fabricrunner'
    },
    {
        'name': 'run-remote-script',
        'description': 'A remote execution runner that executes actions '
                       'as a fixed system user.',
        'enabled': True,
        'runner_parameters': {
            'hosts': {
                'description': 'A comma delimited string of a list of hosts '
                               'where the remote command will be executed.',
                'type': 'string',
                'required': True
            },
            'username': {
                'description': ('Username used to log-in. If not provided, '
                                'default username from config is used.'),
                'type': 'string',
                'required': False
            },
            'password': {
                'description': ('Password used to log in. If not provided, '
                                'private key from the config file is used.'),
                'type': 'string',
                'required': False
            },
            'private_key': {
                'description': ('Private key used to log in. If not provided, '
                                'private key from the config file is used.'),
                'type': 'string',
                'required': False
            },
            'parallel': {
                'description': 'Default to parallel execution.',
                'type': 'boolean',
                'default': True,
                'immutable': True
            },
            'cwd': {
                'description': 'Working directory where the script will be executed in.',
                'type': 'string',
                'default': FABRIC_RUNNER_DEFAULT_REMOTE_DIR
            },
            'env': {
                'description': ('Environment variables which will be available to the script'
                                '(e.g. key1=val1,key2=val2)'),
                'type': 'object'
            },
            'sudo': {
                'description': 'The remote command will be executed with sudo.',
                'type': 'boolean',
                'default': False
            },
            'dir': {
                'description': 'The working directory where the script will be copied to ' +
                               'on the remote host.',
                'type': 'string',
                'default': FABRIC_RUNNER_DEFAULT_REMOTE_DIR
            },
            'kwarg_op': {
                'description': 'Operator to use in front of keyword args i.e. "--" or "-".',
                'type': 'string',
                'default': '--'
            },
            'timeout': {
                'description': ('Action timeout in seconds. Action will get killed if it '
                                'doesn\'t finish in timeout seconds.'),
                'type': 'integer',
                'default': FABRIC_RUNNER_DEFAULT_ACTION_TIMEOUT
            }
        },
        'runner_module': 'st2actions.runners.fabricrunner'
    },
    {
        'name': 'http-runner',
        'description': 'A HTTP client for running HTTP actions.',
        'enabled': True,
        'runner_parameters': {
            'url': {
                'description': 'URL to the HTTP endpoint.',
                'type': 'string',
                'required': True
            },
            'headers': {
                'description': 'HTTP headers for the request.',
                'type': 'string'
            },
            'cookies': {
                'description': 'Optional cookies to send with the request.',
                'type': 'object'
            },
            'http_proxy': {
                'description': 'A URL of a HTTP proxy to use (e.g. http://10.10.1.10:3128).',
                'type': 'string'
            },
            'https_proxy': {
                'description': 'A URL of a HTTPs proxy to use (e.g. http://10.10.1.10:3128).',
                'type': 'string'
            },
            'allow_redirects': {
                'description': 'Set to True if POST/PUT/DELETE redirect following is allowed.',
                'type': 'boolean',
                'default': False
            },
        },
        'runner_module': 'st2actions.runners.httprunner'
    },
    {
        'name': 'mistral-v1',
        'description': 'A runner for executing mistral v1 workflow.',
        'enabled': True,
        'runner_parameters': {
            'workbook': {
                'description': 'The name of the workbook.',
                'type': 'string',
                'required': True
            },
            'task': {
                'description': 'The startup task in the workbook to execute.',
                'type': 'string',
                'required': True
            },
            'context': {
                'description': 'Context for the startup task.',
                'type': 'object',
                'default': {}
            }
        },
        'runner_module': 'st2actions.runners.mistral.v1'
    },
    {
        'name': 'mistral-v2',
        'description': 'A runner for executing mistral v2 workflow.',
        'enabled': True,
        'runner_parameters': {
            'workflow': {
                'description': ('The name of the workflow to run if the entry_point is a '
                                'workbook of many workflows. The name should be in the '
                                'format "<pack_name>.<action_name>.<workflow_name>". '
                                'If entry point is a workflow or a workbook with a single '
                                'workflow, the runner will identify the workflow '
                                'automatically.'),
                'type': 'string'
            },
            'task': {
                'description': 'The name of the task to run for reverse workflow.',
                'type': 'string'
            },
            'context': {
                'description': 'Additional workflow inputs.',
                'type': 'object',
                'default': {}
            }
        },
        'runner_module': 'st2actions.runners.mistral.v2',
        'query_module': 'st2actions.query.mistral.v2'
    },
    {
        'name': 'action-chain',
        'description': 'A runner for launching linear action chains.',
        'enabled': True,
        'runner_parameters': {},
        'runner_module': 'st2actions.runners.actionchainrunner'
    },
    {
        'name': 'run-python',
        'description': 'A runner for launching python actions.',
        'enabled': True,
        'runner_parameters': {
            'env': {
                'description': ('Environment variables which will be available to the script'
                                '(e.g. key1=val1,key2=val2)'),
                'type': 'object'
            },
            'timeout': {
                'description': ('Action timeout in seconds. Action will get killed if it '
                                'doesn\'t finish in timeout seconds.'),
                'type': 'integer',
                'default': PYTHON_RUNNER_DEFAULT_ACTION_TIMEOUT
            }
        },
        'runner_module': 'st2actions.runners.pythonrunner'
    },

    # Experimental runners below
    {
        'name': 'run-windows-cmd',
        'description': 'A remote execution runner that executes commands'
                       'on Windows hosts.',
        'experimental': True,
        'enabled': True,
        'runner_parameters': {
            'host': {
                'description': 'Host to execute the command on',
                'type': 'string',
                'required': True
            },
            'username': {
                'description': 'Username used to log-in.',
                'type': 'string',
                'default': 'Administrator',
                'required': True,
            },
            'password': {
                'description': 'Password used to log in.',
                'type': 'string',
                'required': True
            },
            'cmd': {
                'description': 'Arbitrary command to be executed on the '
                               'remote host.',
                'type': 'string'
            },
            'timeout': {
                'description': ('Action timeout in seconds. Action will get killed if it '
                                'doesn\'t finish in timeout seconds.'),
                'type': 'integer',
                'default': FABRIC_RUNNER_DEFAULT_ACTION_TIMEOUT
            }
        },
        'runner_module': 'st2actions.runners.windows_command_runner'
    },
    {
        'name': 'run-windows-script',
        'description': 'A remote execution runner that executes power shell scripts'
                       'on Windows hosts.',
        'enabled': True,
        'experimental': True,
        'runner_parameters': {
            'host': {
                'description': 'Host to execute the command on',
                'type': 'string',
                'required': True
            },
            'username': {
                'description': 'Username used to log-in.',
                'type': 'string',
                'default': 'Administrator',
                'required': True,
            },
            'password': {
                'description': 'Password used to log in.',
                'type': 'string',
                'required': True
            },
            'share': {
                'description': 'Name of the Windows share where script files are uploaded',
                'type': 'string',
                'required': True,
                'default': 'C$'
            },
            'timeout': {
                'description': ('Action timeout in seconds. Action will get killed if it '
                                'doesn\'t finish in timeout seconds.'),
                'type': 'integer',
                'default': FABRIC_RUNNER_DEFAULT_ACTION_TIMEOUT
            }
        },
        'runner_module': 'st2actions.runners.windows_script_runner'
    }
]


def register_runner_types(experimental=False):
    """
    :param experimental: True to also register experimental runners.
    :type experimental: ``bool``
    """
    LOG.debug('Start : register default RunnerTypes.')

    for runnertype in RUNNER_TYPES:
        runner_name = runnertype['name']
        runner_experimental = runnertype.get('experimental', False)

        if runner_experimental and not experimental:
            LOG.debug('Skipping experimental runner "%s"' % (runner_name))
            continue

        if 'experimental' in runnertype:
            del runnertype['experimental']

        try:
            runnertype_db = get_runnertype_by_name(runner_name)
            update = True
        except StackStormDBObjectNotFoundError:
            runnertype_db = None
            update = False

        runnertype_api = RunnerTypeAPI(**runnertype)
        runnertype_api.validate()
        runner_type_model = RunnerTypeAPI.to_model(runnertype_api)

        if runnertype_db:
            runner_type_model.id = runnertype_db.id

        try:
            runnertype_db = RunnerType.add_or_update(runner_type_model)

            extra = {'runnertype_db': runnertype_db}
            if update:
                LOG.audit('RunnerType updated. RunnerType %s', runnertype_db, extra=extra)
            else:
                LOG.audit('RunnerType created. RunnerType %s', runnertype_db, extra=extra)
        except Exception:
            LOG.exception('Unable to register runner type %s.', runnertype['name'])

    LOG.debug('End : register default RunnerTypes.')
