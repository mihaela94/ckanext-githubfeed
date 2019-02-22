# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "ubuntu/xenial64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 5000, host: 5002

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"
  config.vm.synced_folder "etc/", "/etc/ckan/default"
  # config.vm.synced_folder "src/", "/usr/lib/ckan/default/src"
  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
    vb.memory = "4096"
  end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y python-dev postgresql libpq-dev python-pip python-virtualenv git-core solr-jetty openjdk-8-jdk redis-server
    mkdir -p /home/vagrant/ckan/lib
    sudo ln -s /home/vagrant/ckan/lib /usr/lib/ckan
    mkdir -p /home/vagrant/ckan/etc
    sudo ln -s /home/vagrant/ckan/etc /etc/ckan
    sudo mkdir -p /usr/lib/ckan/default
    sudo chown `whoami` /usr/lib/ckan/default
    sudo mkdir /var/lib/ckan
    sudo chown -R vagrant:vagrant /var/lib/ckan
    sudo chown -R vagrant:vagrant /usr/lib/ckan
    sudo chown -R vagrant:vagrant /usr/lib/ckan/default
    virtualenv --no-site-packages /usr/lib/ckan/default
    . /usr/lib/ckan/default/bin/activate
    pip install setuptools==36.1
    pip install -e 'git+https://github.com/ckan/ckan.git@ckan-2.8.2#egg=ckan'
    pip install -e 'git+https://github.com/code4romania/ckanext-dataportaltheme#egg=ckanext-dataportaltheme'
    pip install -r /usr/lib/ckan/default/src/ckan/requirements.txt
    pip install flask_debugtoolbar
    cd /vagrant
    python setup.py develop
    deactivate
    . /usr/lib/ckan/default/bin/activate
    sudo -u postgres psql -c "CREATE USER ckan_default WITH PASSWORD 'ckan_default';"
    sudo -u postgres createdb -O ckan_default ckan_default -E utf-8
    sudo -u postgres psql -c "GRANT ALL ON DATABASE ckan_default TO ckan_default;"
    cp /etc/ckan/default/pg_hba.conf /etc/postgresql/9.5/main/pg_hba.conf
    sudo service postgresql restart
    cp /etc/ckan/default/jetty8 /etc/default/jetty
    sudo service jetty8 restart
    sudo mv /etc/solr/conf/schema.xml /etc/solr/conf/schema.xml.bak
    sudo ln -s /usr/lib/ckan/default/src/ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml
    sudo service jetty8 restart
    cd /usr/lib/ckan/default/src/ckan
    paster db init -c /etc/ckan/default/development.ini
    sudo chown -R vagrant:vagrant /var/lib/ckan
    sudo chown -R vagrant:vagrant /usr/lib/ckan
  SHELL
end
