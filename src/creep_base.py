from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

BODY_PART_COST = {
    MOVE: 50, WORK: 100, ATTACK: 80,
    CARRY: 50, HEAL: 250, RANGED_ATTACK: 150,
    TOUGH: 10, CLAIM: 600}


def get_part_cost(part_list):
    num = 0
    for part in part_list:
        num += BODY_PART_COST[part]
    return num
