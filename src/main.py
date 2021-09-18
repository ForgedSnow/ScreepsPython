from bots import harvester, builder, spawn_delivery, upgrader
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
def toggle_debug():
    global DEBUG
    DEBUG = False if DEBUG else True
    return DEBUG


#creep related scripts
js_global.delete_creep = scripts.creep_related.delete_creep
js_global.emergency_harvest = scripts.creep_related.emergency_harvest
js_global.clear_creeps = scripts.creep_related.clean_memory

#building scripts
js_global.build_road = scripts.building.plan_road_path
js_global.remove_all_flags = scripts.building.remove_flags

#console variables
js_global.debug = toggle_debug


role_dict = {
    'harvester': harvester.run_harvester,
    'builder': builder.run_builder,
    'spawn_feeder': spawn_delivery.run_spawn_delivery,
    'upgrader': upgrader.run_upgrader,
}

# order in decreasing priority
roles = ['spawn_feeder', 'upgrader', 'builder', 'harvester']


hard_coded_workers = {
    'harvester': 8,
    'spawn_feeder': 2,
    'builder': 5,
    'upgrader': 1
}


role_count = {
    'harvester': -1,
    'spawn_feeder': -1,
    'builder': -1,
    'upgrader': -1
}


def print_roles():
    print(*count_roles())


js_global.print_bots = print_roles


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
        print(role, count)
        out_put.append("{}: {}".format(role, count))
    return out_put


# conditional print. only print if DEBUG is true
def cp(*args):
    if DEBUG:
        print(*args, sep=" ", end="\n")
    return 0


def main():
    """
    Main game logic loop.
    """
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
            for role in roles:
                if role_count[role] < hard_coded_workers[role]:
                    if spawn.spawnCreep([WORK, WORK, MOVE, CARRY], "{}{}".format("Creep-", Game.time), {'memory': {'role': role}}) == 0:
                        print(role, "created")
                        return 0

            # always have one builder
            if spawn.spawnCreep([WORK, WORK, MOVE, CARRY], "BuilderOmega", {'memory': {'role': 'builder'}}) == 0:
                return 0
            if len(Game.creeps) < 1 and spawn.room.energyAvailable >= 250:
                spawn.createCreep([WORK, CARRY, MOVE], "bootstrap")
                boot = Memory.creeps["bootstrap"]
                boot.memory.role = 'harvester'


module.exports.loop = main
