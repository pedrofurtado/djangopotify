Vagrant.configure('2') do |config|
  config.vagrant.plugins = ['vagrant-vbguest', 'vagrant-disksize']
  config.vm.box = 'centos/8'
  config.disksize.size = '50GB'
  config.vbguest.installer_options = { allow_kernel_upgrade: true, reboot_timeout: 5000 }
  config.vm.synced_folder '.', '/vagrant', type: 'virtualbox'
  config.vm.network 'forwarded_port', guest: 4444, host: 4444, id: 'django'

  config.vm.provider 'virtualbox' do |v|
    v.memory = '4096'
    v.cpus = '2'
    v.customize ['setextradata', :id, 'VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root', '1']
  end

  config.vm.provision 'shell', privileged: true, inline: <<-SHELL
    yum install -y cloud-utils-growpart
    sudo growpart /dev/sda 1
    sudo xfs_growfs /

    yum install -y git vim sqlite sqlite-devel postgresql-devel

    yum install -y yum-utils device-mapper-persistent-data lvm2
    yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    yum install -y --nobest docker-ce docker-ce-cli containerd.io
    systemctl start docker
    systemctl enable docker

    docker container run --name postgresql --restart always -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=djangopotify postgres:12

    export PYTHON_VERSION=3.8.5
    yum install -y make tar wget gcc openssl-devel bzip2-devel libffi-devel
    wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz
    tar xzf Python-$PYTHON_VERSION.tgz
    cd Python-$PYTHON_VERSION
    ./configure --enable-optimizations
    make altinstall
    ln -sf /usr/local/bin/python3.8 /usr/bin/python
    ln -sf /usr/local/bin/python3.8 /usr/bin/python3
    ln -sf /usr/local/bin/pip3.8 /usr/bin/pip
    ln -sf /usr/local/bin/pip3.8 /usr/bin/pip3

    cat >> /etc/systemd/system/djangopotify.service << 'EOL'
[Unit]
Description=Djangopotify

[Service]
Type=simple
Restart=always
RestartSec=1
StartLimitInterval=0
ExecStart=/bin/bash -c 'cd /vagrant && python manage.py runserver 0.0.0.0:4444'

[Install]
WantedBy=multi-user.target
EOL

    cat >> /home/vagrant/.bashrc <<EOL
cd /vagrant
sudo su
EOL

    cat >> /home/vagrant/upgrade_dependencies.sh <<EOL
#!/bin/bash
cd /vagrant
pip install --upgrade --force-reinstall -r requirements.txt
pip freeze > requirements.txt
EOL
    chmod +x /home/vagrant/upgrade_dependencies.sh

    cd /vagrant
    pip install -r requirements.txt
    python manage.py migrate
    systemctl daemon-reload
    systemctl start djangopotify.service
    systemctl enable djangopotify.service

    echo "Djangopotify workspace created!"
  SHELL
end
