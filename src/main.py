from bots import harvester, builder, spawn_delivery, upgrader, miner, hauler, tower_bro
from structures import tower_logic, link_logic
# defs is a package which claims to export all constants and some JavaScript objects, but in reality does
#  nothing. This is useful mainly when using an editor like PyCharm, so that it 'knows' that things like Object, Creep,
#  Game, etc. do exist.
from defs import *
import scripts.creep_related
import scripts.building

# These are currently required for Transcrypt in order to use the following names in JavaScript.
# Without the 'noalias' pragma, each of the following would be translated into something like 'py_Infinity' or
#  'py_keys' in the output file.
__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


DEBUG = False


def check_for_portals():
    spawn = Game.spawns["Snow"]
    for id, room in _.pairs(Game.rooms):
        print(room)
    return 0


js_global.portals = check_for_portals


def toggle_debug():
    global DEBUG
    DEBUG = False if DEBUG else True
    return DEBUG


def create_chad(role):
    spawn = Game.spawns["Snow"]
    body = role_body[role](spawn.room.energyAvailable)
    if spawn.spawnCreep(body, "{}{}".format("Creep-", Game.time),
                        {'memory': {'role': role, 'chad': True}}) == 0:
        print("incoming chad", body)
    else:
        print("not enough energy")


#creep related scripts
js_global.delete_creep = scripts.creep_related.delete_creep
js_global.emergency_harvest = scripts.creep_related.emergency_harvest
js_global.clear_creeps = scripts.creep_related.clean_memory
js_global.create_chad = create_chad

#building scripts
js_global.build_road = scripts.building.plan_road_path
js_global.remove_all_flags = scripts.building.remove_flags

js_global.new_container = scripts.building.plan_container
js_global.new_storage = scripts.building.plan_storage
js_global.new_road = scripts.building.plan_road

#console variables
js_global.debug = toggle_debug


role_dict = {
    'harvester': harvester.run_harvester,
    'builder': builder.run_builder,
    'spawn_feeder': spawn_delivery.run_spawn_delivery,
    'upgrader': upgrader.run_upgrader,
    'miner': miner.run_miner,
    'hauler': hauler.run_hauler,
    'tower_bro': tower_bro.run_tower_bro,
}

# order in decreasing priority
roles = ['hauler', 'miner', 'tower_bro', 'spawn_feeder', 'upgrader', 'builder', 'harvester']


hard_coded_workers = {
    'harvester': 0,
    'spawn_feeder': 0,
    'builder': 0,
    'upgrader': 1,
    'miner': 2,
    'hauler': 2,
    'tower_bro': 1,
}


role_count = {
    'harvester': -1,
    'spawn_feeder': -1,
    'builder': -1,
    'upgrader': -1,
    'miner': -1,
    'hauler': -1,
    'tower_bro': -1,
}


role_body = {
    'harvester': harvester.make_parts,
    'builder': builder.make_parts,
    'spawn_feeder': spawn_delivery.make_parts,
    'upgrader': upgrader.make_parts,
    'miner': miner.make_parts,
    'hauler': hauler.make_parts,
    'tower_bro': tower_bro.make_parts,
}


def create(role):
    spawn = Game.spawns["Snow"]
    body = role_body[role](spawn.room.energyAvailable)
    if spawn.spawnCreep(body, "{}{}".format("Creep-", Game.time),
                        {'memory': {'role': role}}) == 0:
        print("creep order fulfilled")
    else:
        print("not enough energy")


js_global.create = create


def print_roles():
    print(*count_roles(), sep="")
    return 0


js_global.print_bots = print_roles


def body_cost(body):
    cost = 0
    for part in body:
        cost += BODYPART_COST[part]
    return cost


def culling_time(role, amount):
    count = 0
    for bot in _.filter(Object.keys(Game.creeps), lambda x: Game.creeps[x].memory.role is role):
        Game.creeps[bot].suicide()
        count += 1
        if count >= amount:
            print("Culled", count, role, "robots")
            return 0
    print("Culled only", count, role, "robots")


js_global.culling = culling_time


def count_roles():
    out_put = []
    # count roles
    for role in _.keys(hard_coded_workers):
        count = len(_.filter(Object.keys(Game.creeps), lambda x: Game.creeps[x].memory.role is role))
        _.set(role_count, role, count)
        out_put.append("{}: {}\n".format(role, count))
    return out_put


# conditional print. only print if DEBUG is true
def cp(*args):
    if DEBUG:
        print(*args, sep=" ", end="\n")
    return 0


def find_structures(structure, room):
    return room.find(FIND_STRUCTURES, {"filter": lambda x: x.structureType == structure})
    # return _.filter(room.find(FIND_STRUCTURES), lambda x: x.structureType == structure)


def main():
    """
    Main game logic loop.
    """
    #run towers
    for tower in _.filter(Game.spawns["Snow"].room.find(FIND_STRUCTURES), lambda x: x.structureType == STRUCTURE_TOWER):
        tower_logic.run_tower(tower)
    #  print(_.filter(Game.spawns["Snow"].room.find(FIND_STRUCTURES), lambda x: x.structureType == STRUCTURE_TOWER))

    #  run links
    for link in Game.spawns["Snow"].room.find(FIND_STRUCTURES, {"filter": lambda x: x.structureType == STRUCTURE_LINK}):
        if link.pos.x == 15 and link.pos.y == 40:
            link_logic.run_link(link)
    # link = Game.spawns["Snow"].room.find(FIND_STRUCTURES, {"filter": lambda x: x.structureType == STRUCTURE_LINK})[0]
    # link_logic.run_link(link)

    # Run each creep
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        role = creep.memory.role
        if role in role_dict:
            try:
                role_dict[role](creep)
            except:
                cp(creep, "bad role function")
        else:
            cp("bad role", role)

    scripts.creep_related.clean_memory()

    # count roles
    for role in _.keys(hard_coded_workers):
        count = len(_.filter(Object.keys(Game.creeps), lambda x: Game.creeps[x].memory.role is role))
        _.set(role_count, role, count)

    # Run each spawn
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        if not spawn.spawning:
            if spawn.room.energyAvailable < 300:
                break
            for role in roles:
                dynamic_count = 0
                if role is "upgrader":
                    storage = spawn.room.storage

                    def dynamic_count(ratio):
                        if ratio > 0.99:
                            return 6
                        if ratio > 0.9:
                            return 4
                        if ratio > 0.75:
                            return 3
                        if ratio > 0.5:
                            return 2
                        if ratio > 0.1:
                            return 1
                        return 0
                    dynamic_count = dynamic_count(storage.store.getUsedCapacity(RESOURCE_ENERGY)
                                                  / storage.store.getCapacity(RESOURCE_ENERGY))

                if role_count[role] < hard_coded_workers[role] + dynamic_count:
                    print("energy", spawn.room.energyAvailable)
                    '''
                    if spawn.spawnCreep([WORK, WORK, MOVE, CARRY], "{}{}".format("Creep-", Game.time), {'memory': {'role': role}}) == 0:
                        print(role, "created")
                        return 0
                    '''
                    body = role_body[role](spawn.room.energyAvailable)
                    if spawn.spawnCreep(body, "{}{}".format("Creep-", Game.time),
                                        {'memory': {'role': role}}) == 0:
                        print(role, body, "created. Cost:", body_cost(body))
                        return 0
                    else:
                        print(body, "too expensive")

            if len(Game.creeps) < 1 and spawn.room.energyAvailable >= 250:
                spawn.createCreep([WORK, CARRY, MOVE], "bootstrap")
                boot = Memory.creeps["bootstrap"]
                boot.memory.role = 'harvester'


module.exports.loop = main
