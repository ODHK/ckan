from openplatform import *

## GLOBALS

env.project_name = 'ckan'             	# e.g. 'opengov'
env.project_url = 'data.opendatahk.com' # e.g. 'opengov.hk'
env.hosts = ['128.199.212.155']       	# default to open platform
env.path = '/var/www/%(project_url)s' % env
env.user = 'su_' + project_name             

env.github_account = 'ODHK'             # e.g. 'ODHK'
env.github_repo = 'ckan'                # e.g. 'opengov.hk'
env.setup_github = False

env.key_filename = "~/.ssh/id_rsa"
env.colorize_errors = True
env.env_file = "requirements.txt"

## ENVIRONMENTS

def platform():
    "Use the open platform"
    env.hosts = ['opendatahk.com']
    env.user = 'su_%(project_name)s' % env
    env.path = '/var/www/%(project_url)s' % env
    env.env_file = "requirements.txt"
    env.github_email = 'info@opendatahk.com'
    env.github_name = 'ODHK Admin'
    env.setup_github = True
    paths()

# Setup

def setup_ubuntu():
    """
    Update the Ubuntu host and install the necessary third party software, then
    follow the setup steps all OSes have in common
    """
    sudo('apt-get install -y python-setuptools python-dev')
    sudo('easy_install pip')
    sudo('pip install virtualenv')
    sudo('apt-get install -y git zsh htop links')
    sudo('apt-get install -y nginx')
    sudo('apt-get install -y postgresql postgresql-contrib python-psycopg2 libpq-dev')
    sudo('apt-get install -y libxml2 libxslt1.1 libxslt1-dev')
    setup_common()

def setup_fedora():
    """
    Update the Fedora host and install the necessary third party software, then
    follow the setup steps all OSes have in common
    """
    sudo('yum install -y python-devel python-pip')
    sudo('pip install virtualenv')
    sudo('yum install -y nginx git postgresql postgresql-devel postgresql-server libxml2 libxml2-python')
    setup_common()

def setup_osx():
    """
    Requires brew. Update the OSX host and install the necessary third party software, then
    follow the setup steps all OSes have in common.
    """
    sudo('easy_install pip')
    sudo('pip install virtualenv')
    sudo('brew install nginx')
    setup_common()

def setup_common():
    setup_user_dir()
    setup_github()
    prepare_nginx()
    setup_release_dirs()
    deploy()