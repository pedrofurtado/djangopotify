Vagrant.configure('2') do |config|
  config.vagrant.plugins = ['vagrant-vbguest', 'vagrant-disksize']
  config.vm.box = 'centos/8'
  config.disksize.size = '50GB'
  config.vbguest.installer_options = { allow_kernel_upgrade: true, reboot_timeout: 5000 }
  config.vm.synced_folder '.', '/vagrant', type: 'virtualbox'
  config.vm.network 'forwarded_port', guest: 4444, host: 4444, id: 'django'
  config.vm.network 'forwarded_port', guest: 4445, host: 4445, id: 'mailer'

  config.vm.provider 'virtualbox' do |v|
    v.memory = '4096'
    v.cpus = '2'
    v.customize ['setextradata', :id, 'VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root', '1']
  end

  config.vm.provision 'shell', privileged: true, inline: <<-SHELL
    yum install -y cloud-utils-growpart
    sudo growpart /dev/sda 1
    sudo xfs_growfs /

    yum check-update -y
    yum update -y
    yum -y install epel-release
    yum check-update -y
    yum update -y
    yum config-manager --set-enabled PowerTools
    yum install -y usbutils dos2unix git cronie vim curl curl-devel tar wget lynx sed zip unzip openssh-server htop gpg gnupg2 make gcc gcc-c++ epel-release yum-utils
    yum groupinstall -y 'Development Tools'
    systemctl enable sshd
    systemctl start sshd

    yum install -y git vim sqlite sqlite-devel postgresql-devel

    yum install -y yum-utils device-mapper-persistent-data lvm2
    yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    yum install -y --nobest docker-ce docker-ce-cli containerd.io
    systemctl start docker
    systemctl enable docker

    docker container run --name postgresql --restart always -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=djangopotify postgres:12
    docker container run --name mailer     --restart always -d -p 4445:8025 -p 3006:1025 mailhog/mailhog

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
ExecStart=/bin/bash -c 'cd /vagrant && source /etc/profile.d/djangopotify-envs.sh && python manage.py runserver 0.0.0.0:4444'

[Install]
WantedBy=multi-user.target
EOL

    cat >> /etc/profile.d/djangopotify-envs.sh <<EOL
#!/bin/bash

export DJANGOPOTIFY_EMAIL_USE_TLS=no
export DJANGOPOTIFY_EMAIL_PORT=3006
export DJANGOPOTIFY_EMAIL_HOST=localhost
export DJANGOPOTIFY_EMAIL_HOST_USER=''
export DJANGOPOTIFY_EMAIL_HOST_PASSWORD=''
EOL
    chmod +x /etc/profile.d/djangopotify-envs.sh
    source /etc/profile.d/djangopotify-envs.sh

    cat >> /home/vagrant/.bashrc <<EOL
cd /vagrant
sudo su
source /etc/profile.d/djangopotify-envs.sh
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
