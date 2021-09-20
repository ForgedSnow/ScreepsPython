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
    #  parts = [WORK, CARRY, MOVE, MOVE]
    parts = [CARRY, WORK, WORK, MOVE]
    count = max_energy - 300
    if max_energy <= 300:
        return parts
    if max_energy >= 900:
        return [WORK, WORK, WORK, WORK, WORK, WORK, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE]
    while count >= 50:
        if count >= 50:
            parts.append(CARRY)
            count -= 50
        if count >= 100:
            parts.append(WORK)
            count -= 100
        if count >= 50:
            parts.append(MOVE)
            count -= 50
    return parts


def run_upgrader(creep):
    if creep.memory.chad:
        run_chad_upgrader(creep)
        return 0
    run_chad_upgrader(creep)
    '''return 0'''
    '''if not creep.memory.working and creep.store[RESOURCE_ENERGY] == 0:
        creep.memory.working = True
        creep.say('collecting')
    if creep.memory.working and creep.store.getFreeCapacity() == 0:
        creep.memory.working = False
        creep.say('upgrading')
    if creep.memory.working:
        nearest = creep.pos.findClosestByRange(FIND_SOURCES_ACTIVE)
        if creep.harvest(nearest) == ERR_NOT_IN_RANGE:
            creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ffaa00'}})
    else:
        if creep.upgradeController(creep.room.controller) == ERR_NOT_IN_RANGE:
            creep.moveTo(creep.room.controller)
            '''


def run_chad_upgrader(creep):
    if not creep.memory.working and creep.store[RESOURCE_ENERGY] == 0:
        creep.memory.working = True
        creep.say('collecting')
    if creep.memory.working and creep.store.getFreeCapacity() <= 20:
        creep.memory.working = False
        creep.say('upgrading')
    if creep.memory.working:
        '''
        nearest = creep.pos.findClosestByRange(
            _.filter(creep.room.find(FIND_STRUCTURES),
                     lambda x: (x.structureType is STRUCTURE_STORAGE or x.structureType is STRUCTURE_CONTAINER)
                               and x.store.getUsedCapacity() > 0))
        '''
        nearest = creep.room.find(FIND_STRUCTURES,
                                  {"filter": lambda structure: structure.pos.x == 10 and structure.pos.y == 5})[0]
        #  print(nearest)
        if nearest:
            if nearest.store.getUsedCapacity(RESOURCE_ENERGY) == 0:
                nearest = creep.room.find(FIND_SOURCES)[0]
                if creep.harvest(nearest) == ERR_NOT_IN_RANGE:
                    creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ffaa00'}})

            elif creep.withdraw(nearest, RESOURCE_ENERGY) == ERR_NOT_IN_RANGE:
                creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ffaa00'}})
            else:
                #  print(creep.withdraw(nearest, RESOURCE_ENERGY), "withdraw returned")
                pass
    else:
        if creep.upgradeController(creep.room.controller) == ERR_NOT_IN_RANGE:
            creep.moveTo(creep.room.controller)
