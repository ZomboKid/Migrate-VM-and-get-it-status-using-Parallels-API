#! /usr/bin/python

import sys
import prlsdkapi
#import inspect

new_host_ip="127.0.0.1"
new_host_user="user"
new_host_passwd="password"

vm_name="vm"

consts = prlsdkapi.prlsdk.consts
#---------------------------------------------------------------------------------------
#Retrieves name of const by its value from prlsdkapi.prlsdk.consts 
def retrieve_name(var):
    module=globals().get("consts", None)
    book = {}
    if module:
        book = {key: value for key, value in module.__dict__.iteritems() if not (key.startswith('__') or key.startswith('_'))}
    return (''.join([k for k,v in book.items() if v == var])).replace("VMS_","")
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
def getstate_vm(HOST,USER,PASSW,VM):
    prlsdkapi.init_server_sdk()
    server = prlsdkapi.Server()
    server.login(HOST,USER,PASSW, '', 0, 0, consts.PSL_NORMAL_SECURITY).wait()

    vm = get_vm(server,VM)

    vm_st=int(vm.get_state().wait().get_param().get_state())
 
    print "VM state is:",retrieve_name(vm_st)

    server.logoff()
    prlsdkapi.deinit_sdk()
#---------------------------------------------------------------------------------------
def main():
    getstate_vm(new_host_ip,new_host_user,new_host_passwd,vm_name)
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

