from openplatform import *

## GLOBALS

env.project_name = 'ckan'               # e.g. 'opengov'
env.project_url = 'data.opendatahk.com' # e.g. 'opengov.hk'
env.hosts = ['128.199.212.155']         # default to open platform
env.path = '/var/www/%(project_url)s' % env
env.user = 'su_%(project_name)s' % env            

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

def env_activate():
    run('. /usr/lib/ckan/default/bin/activate')

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
    sudo('apt-get install -y apache2 libapache2-mod-wsgi')
    sudo('apt-get install -y postgresql postgresql-contrib python-psycopg2 libpq-dev libpq5')
    setup_common()

def setup_fedora():
    """
    INCOMPLETE
    Update the Fedora host and install the necessary third party software, then
    follow the setup steps all OSes have in common
    """
    sudo('yum install -y python-devel python-pip')
    sudo('pip install virtualenv')
    sudo('yum install -y nginx git postgresql postgresql-devel postgresql-server libxml2 libxml2-python')
    setup_common()

def setup_osx():
    """
    INCOMPLETE
    Requires brew. Update the OSX host and install the necessary third party software, then
    follow the setup steps all OSes have in common.
    """
    sudo('easy_install pip')
    sudo('pip install virtualenv')
    sudo('brew install nginx')
    setup_common()

def setup_ckan_package():
    """
    Install CKAN from repository

    http://docs.ckan.org/en/1197-rtd-fix/install-from-package.html
    """
    require('hosts', provided_by=[localhost,platform])

    setup_ubuntu()

    run('wget http://packaging.ckan.org/python-ckan_2.0_amd64.deb')
    sudo('sudo dpkg -i python-ckan_2.0_amd64.deb')

def setup_solr_jetty():
    sudo('sudo apt-get -y install openjdk-7-jdk')
    with settings(warn_only=True):
        sudo('mkdir /usr/java')
    sudo('ln -s /usr/lib/jvm/java-7-openjdk-amd64 /usr/java/default')
    sudo('apt-get install -y solr-jetty')


def setup_ckan_source():
    """
    Install CKAN from source for Ubuntu 14.04

    http://docs.ckan.org/en/1197-rtd-fix/install-from-source.html
    https://www.digitalocean.com/community/articles/how-to-install-solr-on-ubuntu-14-04
    """
    require('hosts', provided_by=[localhost,platform])

    setup_ubuntu()
    setup_solr_jetty()
    sudo('mkdir -p /usr/lib/ckan/default')
    sudo('chown -R `whoami` /usr/lib/ckan')
    sudo('chmod -R u+rwx /usr/lib/ckan')
    run('virtualenv --no-site-packages /usr/lib/ckan/default')
    env_activate()

    run("pip install -e 'git+https://github.com/ckan/ckan.git@ckan-2.2#egg=ckan'")
    run('pip install -r /usr/lib/ckan/default/src/ckan/requirements.txt')

    run('deactivate')
    env_activate()

def setup_ckan_production():
    # Too dangerous to not do manually.
    # Followed http://ckan-docs-tw.readthedocs.org/en/latest/deployment.html
    # C.F. http://blog.talatchaudhri.net/2014/03/27/uwsgi-nginx-ckan/
    setup_ckan_source()
    sudo('apt-get install -y postfix')


def setup_common():
    setup_user_dir()
    setup_github()
    prepare_nginx()
    setup_release_dirs()