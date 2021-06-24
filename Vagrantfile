# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/focal64"

  config.vm.provider :virtualbox do |v|
    v.name = "dockervm"
    v.memory = 4096
    v.cpus = 2
    v.linked_clone = true
  end
  config.vm.hostname="dockervm"
  config.vm.synced_folder "./code", "./code", disabled: true

  # Ansible provisioner.
  config.vm.provision "ansible" do |ansible|
    ansible.compatibility_mode = "2.0"
    ansible.playbook = "playbook.yml"
    ansible.become = true
  end

end
