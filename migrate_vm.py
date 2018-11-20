#! /usr/bin/python

import sys
import prlsdkapi
import inspect

old_host_ip="127.0.0.11"
old_host_user="user"
old_host_passwd="password"

new_host_ip="127.0.0.12"
new_host_user="user"
new_host_passwd="password"

vm_name="vm"

consts = prlsdkapi.prlsdk.consts
#---------------------------------------------------------------------------------------
def get_vm(server,vm_name):
    result = server.get_vm_list().wait()
# Iterate through all VMs until we find the one we're looking for
    for i in range(result.get_params_count()):
        vm = result.get_param_by_index(i)
        name = vm.get_name()
        if name.startswith(vm_name):
            return vm
    print "VM",vm_name,"not found on Virtualisation Host",server.get_server_info().get_host_name()
#---------------------------------------------------------------------------------------
def migrate_vm(OLD_HOST,OLD_HOST_USER,OLD_HOST_PASSW,NEW_HOST,NEW_HOST_USER,NEW_HOST_PASSW,VM):
    prlsdkapi.init_server_sdk()
    old_server = prlsdkapi.Server()
    old_server.login(OLD_HOST,OLD_HOST_USER,OLD_HOST_PASSW, '', 0, 0, consts.PSL_NORMAL_SECURITY).wait()

    vm = get_vm(old_server,VM)

    new_server=prlsdkapi.Server()
    new_server.login(NEW_HOST,NEW_HOST_USER,NEW_HOST_PASSW, '', 0, 0, consts.PSL_NORMAL_SECURITY).wait()
   
    print "--------------------------------------------"
    print "Migration vm",VM,"from",OLD_HOST,"to",NEW_HOST,"is in progress..." 
    vm.migrate(new_server).wait()
    print "Migration over Parallels SDK job is complete"
    print "--------------------------------------------"
    
    old_server.logoff()
    new_server.logoff()
    prlsdkapi.deinit_sdk()
#---------------------------------------------------------------------------------------
def main():
    migrate_vm(old_host_ip,old_host_user,old_host_passwd,new_host_ip,new_host_user,new_host_passwd,vm_name)
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

