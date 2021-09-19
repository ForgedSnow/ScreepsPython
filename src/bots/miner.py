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
    parts = [WORK, WORK, MOVE]
    count = max_energy - 300
    if max_energy <= 300:
        return [WORK, WORK, MOVE]
    if max_energy >= 600:
        return [WORK, WORK, WORK, WORK, WORK, MOVE, MOVE]
    while count >= 100:
        if count >= 100:
            parts.append(WORK)
            count -= 100
    return parts


def run_miner(creep):
    if not creep.memory.working and creep.store[RESOURCE_ENERGY] == 0:
        creep.memory.working = True
        creep.say('mining')
    if creep.memory.working and creep.store.getFreeCapacity() == 0:
        creep.memory.working = False
        creep.say('waiting')
    if creep.memory.working:
        nearest = creep.pos.findClosestByRange(FIND_SOURCES_ACTIVE)
        if creep.harvest(nearest) == ERR_NOT_IN_RANGE:
            creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ffaa00'}})
    else:
        pass
