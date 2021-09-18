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
    path = this.findPath(point1, point2, {'ignoreDestructibleStructures': 'true', 'ignoreCreeps': 'true'})
    for i in range(path.length):
        Game.spawns["Snow"].room.createConstructionSite(path[i].x, path[i].y, STRUCTURE_ROAD)
    return 0
