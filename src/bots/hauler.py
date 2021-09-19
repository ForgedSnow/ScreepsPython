from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def make_parts(max_energy):
    parts = [CARRY, CARRY, CARRY, MOVE, MOVE, MOVE]
    count = max_energy - 300
    if max_energy <= 300:
        return [CARRY, CARRY, CARRY, MOVE, MOVE, MOVE]
    while count >= 100:
        if count >= 100:
            parts.append(CARRY)
            parts.append(MOVE)
            count -= 100
    return parts


def run_hauler(creep):
    if not creep.memory.working and creep.store[RESOURCE_ENERGY] == 0:
        creep.memory.working = True
        creep.say('collect')
    if creep.memory.working and creep.store.getFreeCapacity() == 0:
        creep.memory.working = False
        creep.say('store')
    if creep.memory.working:
        nearest = creep.pos.findClosestByRange(FIND_DROPPED_RESOURCES)
        if creep.pickup(nearest) == ERR_NOT_IN_RANGE:
            creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ffaa00'}})
    else:
        nearest = creep.pos.findClosestByRange(_.filter(creep.room.find(FIND_STRUCTURES),
                     lambda x: (x.structureType == STRUCTURE_EXTENSION or x.structureType == STRUCTURE_SPAWN)
                    and x.store.getFreeCapacity(RESOURCE_ENERGY) > 0))
        if nearest is None:
            nearest = creep.pos.findClosestByRange(_.filter(creep.room.find(FIND_STRUCTURES),
                      lambda x: (
                        x.structureType == STRUCTURE_CONTAINER or x.structureType == STRUCTURE_STORAGE)
                        and x.store.getFreeCapacity(RESOURCE_ENERGY) > 0))
        if creep.transfer(nearest, RESOURCE_ENERGY) == ERR_NOT_IN_RANGE:
            creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ffaa00'}})
