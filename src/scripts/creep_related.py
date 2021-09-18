from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def delete_creep(name):
    del Memory.creeps[name]
    return 0


'''
def delete_all_creep_memory():
    num = 0
    for name in Object.keys(Game.creeps):
        num += 1
        Memory.creeps.pop(0)
    print("deleted memory from", num, "creeps")
    return 0
for(var i in Memory.creeps) {
    if(!Game.creeps[i]) {
        delete Memory.creeps[i];
    }
}
'''


def emergency_harvest():
    num = 0
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        creep.memory.role = 'harvester'
        num += 1
    print(num, "creeps assigned to harvesting")
    return 0
