from contextlib import contextmanager as _contextmanager
from fabric.context_managers import prefix
from fabric.operations import get, run, sudo
from fabric.state import env
from fabric.contrib import django

django.project('elbtest')
from django.conf import settings

environments = {
    'production': {
        'hosts': ['ubuntu@ec2-54-242-4-78.compute-1.amazonaws.com:22'],
        'source_code': '/home/ubuntu/www/segurosdigitales.com/segurosdigitales',
        'supervisor_commands': [
            'supervisorctl restart celery-segurosdigitales.com',
            'supervisorctl restart segurosdigitales.com',
        ],
        'virtualenv': {
            'virtualenv_name': 'segurosdigitales.com',
            'virtualenv_sh': '/usr/local/bin/virtualenvwrapper.sh',
        },
        'git': {
            'parent': 'origin',
            'branch': 'master',
        }
    }
}

# Utils
@_contextmanager
def virtualenv():
    """ Wrapper to run commands in the virtual env context """
    environment = environments['default']
    workon_home = environment['virtualenv'].get('workon_home',
                                                '~/.virtualenvs')
    with prefix('export WORKON_HOME={0}'.format(workon_home)):
        virtualenv_sh = environment['virtualenv'].get('virtualenv_sh',
                                                      '/etc/bash_completion.d/virtualenvwrapper')
        with prefix('source {0}'.format(virtualenv_sh)):
            virtualenv_name = environment['virtualenv'].get('virtualenv_name')
            with prefix('workon {0}'.format(virtualenv_name)):
                source_code = environment['source_code']
                with prefix('cd {0}'.format(source_code)):
                    yield


def django(command):
    with virtualenv():
        full_command = 'python manage.py {0}'.format(command)
        run(full_command)


# setup
def production():
    environments['default'] = environments['production']
    env.hosts = environments['production']['hosts']
    env.key_filename = 'cmhosts.pem'


#tasks
def test_connection():
    run('uname -a')


def git_pull():
    with virtualenv():
        run('git pull %s %s' % (environments['default']['git']['parent'],
                                environments['default']['git']['branch']))
        #run('git pull')


def pip_install():
    with virtualenv():
        run('pip install -r requirements.txt')


def migrate_list():
    django('migrate --list')


def migrate():
    django('syncdb')
    django('migrate')


def collect_static():
    django('collectstatic --noinput')


def pyclean():
    with virtualenv():
        run('find . -type f -name "*.py[co]" -exec rm -f \{\} \;')


def supervisor_restart():
    for supervisor in environments['default']['supervisor_commands']:
        sudo(supervisor)


def deploy():
    #test_connection()
    git_pull()
    #collect_static()
    pyclean()
    supervisor_restart()


def freem():
    run('free -m')