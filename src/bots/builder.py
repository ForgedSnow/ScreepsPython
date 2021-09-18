from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run_builder(creep):
    if creep.memory.building and creep.store[RESOURCE_ENERGY] == 0:
        creep.memory.building = False
        creep.say('🔄 harvest')

    if not creep.memory.building and creep.store.getFreeCapacity() == 0:
        creep.memory.building = True
        creep.say('🚧 build')

    if creep.memory.building:
        nearest = creep.pos.findClosestByRange(FIND_CONSTRUCTION_SITES)
        if creep.build(nearest) == ERR_NOT_IN_RANGE:
            creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ffffff'}})
    else:
        nearest = creep.pos.findClosestByRange(FIND_SOURCES_ACTIVE)
        if creep.harvest(nearest) == ERR_NOT_IN_RANGE:
            creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ffaa00'}})
