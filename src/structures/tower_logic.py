from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run_tower(tower):
    #  shoot invaders, first priority
    closest_enemy = tower.pos.findClosestByRange(
        _.filter(tower.room.find(FIND_CREEPS),
                 lambda creep: not creep.my))
    if closest_enemy:
        tower.attack(closest_enemy)
        return 0

    #  heal friendlies, second priority
    closest_harmed = tower.pos.findClosestByRange(
        _.filter(tower.room.find(FIND_CREEPS),
                 lambda creep: creep.hits < creep.hitsMax)
    )
    if closest_harmed:
        tower.heal(closest_harmed)

    #  repair structures, third priority
    lowest_health = tower.pos.findClosestByRange(
        _.filter(tower.room.find(FIND_STRUCTURES),
                 lambda structure: structure.hits < 4000 and structure.hitsMax >= 4000 or
                                   (structure.structureType is STRUCTURE_CONTAINER and structure.hits < 225000)),
    )
    if lowest_health:
        tower.repair(lowest_health)
    else:
        pass
