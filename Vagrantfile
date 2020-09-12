Vagrant.configure('2') do |config|
  config.vagrant.plugins = ['vagrant-vbguest', 'vagrant-disksize']
  config.vm.box = 'centos/8'
  config.disksize.size = '50GB'
  config.vbguest.installer_options = { allow_kernel_upgrade: true, reboot_timeout: 5000 }
  config.vm.synced_folder '.', '/vagrant', type: 'virtualbox'
  config.vm.network 'forwarded_port', guest: 8000, host: 8000, id: 'django'

  config.vm.provider 'virtualbox' do |v|
    v.memory = '4096'
    v.cpus = '2'
    v.customize ['setextradata', :id, 'VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root', '1']
  end
=begin
  config.vm.provision 'shell', privileged: true, inline: <<-SHELL
    yum install -y cloud-utils-growpart
    sudo growpart /dev/sda 1
    sudo xfs_growfs /

    yum install -y sqlite sqlite-devel

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

    export DJANGO_VERSION=3.1.1
    pip install Django==$DJANGO_VERSION
    ln -sf /usr/local/bin/django-admin /usr/bin/django-admin

    cat >> /etc/systemd/system/django_python_workout.service << 'EOL'
[Unit]
Description=Django Python Workout

[Service]
Type=simple
Restart=always
RestartSec=1
StartLimitInterval=0
ExecStart=/bin/bash -c 'cd /vagrant && python manage.py runserver 0.0.0.0:8000'

[Install]
WantedBy=multi-user.target
EOL

    cat >> /home/vagrant/.bashrc <<EOL
cd /vagrant
sudo su
EOL

    systemctl daemon-reload
    systemctl start django_python_workout.service
    systemctl enable django_python_workout.service

    echo "Django Python Workout created!"
  SHELL
=end
end
