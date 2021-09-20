from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run_link(source):
    for link in Game.spawns["Snow"].room.find(FIND_STRUCTURES, {"filter": lambda x: x.structureType == STRUCTURE_LINK}):
        if link.pos.x == 10 and link.pos.y == 5 and source.store.getFreeCapacity(RESOURCE_ENERGY) == 0 and link.store.getUsedCapacity(RESOURCE_ENERGY) == 0:
            source.transferEnergy(link)
