from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run_spawn_delivery(creep):
    if not creep.memory.working and creep.store[RESOURCE_ENERGY] == 0:
        creep.memory.working = True
        creep.say('collecting')
    if creep.memory.working and creep.store.getFreeCapacity() == 0:
        creep.memory.working = False
        creep.say('working')
    if creep.memory.working:
        '''sources = creep.room.find(FIND_SOURCES)
        def temp(s):
            return creep.pos.getRangeTo(s)
        nearest = _.sortBy(sources, temp)'''
        nearest = creep.pos.findClosestByRange(FIND_SOURCES_ACTIVE)
        if creep.harvest(nearest) == ERR_NOT_IN_RANGE:
            creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ffaa00'}})
    else:
        if creep.transfer(Game.spawns['Snow'], RESOURCE_ENERGY) == ERR_NOT_IN_RANGE:
            creep.moveTo(Game.spawns['Snow'])
