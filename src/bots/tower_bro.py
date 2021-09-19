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
    if count > 600:
        count = 600
    if max_energy <= 300:
        return parts
    while count >= 50:
        if count >= 50:
            parts.append(CARRY)
            count -= 50
        if count >= 50:
            parts.append(MOVE)
            count -= 50
    return parts


def run_tower_bro(creep):
    if creep.memory.building and creep.store[RESOURCE_ENERGY] == 0:
        creep.memory.building = False
        creep.say('collect')

    if not creep.memory.building and creep.store.getFreeCapacity() == 0:
        creep.memory.building = True
        creep.say('build')

    if creep.memory.building:
        nearest = creep.pos.findClosestByRange(_.filter(creep.room.find(FIND_STRUCTURES),
           lambda x: (x.structureType == STRUCTURE_TOWER)))
        if nearest is None:
            print("no nearest")
        if creep.transfer(nearest, RESOURCE_ENERGY) == ERR_NOT_IN_RANGE:
            creep.moveTo(nearest)
    else:
        nearest = creep.pos.findClosestByRange(_.filter(creep.room.find(FIND_STRUCTURES),
                        lambda x: (x.structureType == STRUCTURE_CONTAINER or x.structureType == STRUCTURE_STORAGE)
                                  and x.store.getUsedCapacity() > 0))
        #  print(creep, "builder", nearest)
        if creep.withdraw(nearest, RESOURCE_ENERGY) == ERR_NOT_IN_RANGE:
            creep.moveTo(nearest)
