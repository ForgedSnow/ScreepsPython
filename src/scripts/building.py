from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def plan_road_path(flag1, flag2):
    point1 = Game.flags[flag1].pos
    point2 = Game.flags[flag2].pos
    #path = this.findPathTo(point1, point2, {'ignoreDestructibleStructures': 'true', 'ignoreCreeps': 'true'})
    path = PathFinder.search(point1, point2, {'ignoreDestructibleStructures': 'true', 'ignoreCreeps': 'true'}).path
    for i in path:
        Game.spawns["Snow"].room.createConstructionSite(i.x, i.y, STRUCTURE_ROAD)
    return 0


def plan_storage(x, y):
    Game.spawns["Snow"].room.createConstructionSite(x, y, STRUCTURE_STORAGE)


def plan_road(x, y):
    Game.spawns["Snow"].room.createConstructionSite(x, y, STRUCTURE_ROAD)


def plan_container(x, y):
    Game.spawns["Snow"].room.createConstructionSite(x, y, STRUCTURE_CONTAINER)


def remove_flags():
    for key, value in _.pairs(Game.flags):
        Game.flags[key].remove()
    return 0
