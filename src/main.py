from bots import harvester, builder
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


#creep related scripts
js_global.delete_creep = scripts.creep_related.delete_creep
js_global.emergency_harvest = scripts.creep_related.emergency_harvest

#building scripts
js_global.build_road = scripts.building.plan_road_path
js_global.remove_all_flags = scripts.building.remove_flags


role_dict = {
    'harvester': harvester.run_harvester,
    'builder': builder.run_builder,
}


def main():
    """
    Main game logic loop.
    """
    # Run each creep
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        role = creep.memory.role
        if role in role_dict:
            role_dict[role](creep)
        else:
            print("bad role: " + role)

    # Run each spawn
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        if not spawn.spawning:
            # always have one builder
            creep_name = "{}{}".format("harvester-", Game.time)
            spawn.spawnCreep([WORK, WORK, MOVE, CARRY], creep_name, {'memory': {'role': 'builder'}})
            # Get the number of our creeps in the room.
            num_creeps = _.sum(Game.creeps, lambda c: c.pos.roomName == spawn.pos.roomName)
            # If there are no creeps, spawn a creep once energy is at 250 or more
            if num_creeps < 1 and spawn.room.energyAvailable >= 250:
                spawn.createCreep([WORK, CARRY, MOVE], "bootstrap")
                boot = Memory.creeps["bootstrap"]
                boot.memory.role = 'harvester'
            # If there are less than 15 creeps but at least one, wait until all spawns and extensions are full before
            # spawning.
            elif num_creeps < 15 and spawn.room.energyAvailable >= spawn.room.energyCapacityAvailable:
                # If we have more energy, spawn a bigger creep.
                #spawn max size creep
                if spawn.room.energyCapacityAvailable >= 350:
                    parts = [WORK, WORK]
                    wiggle_room = spawn.room.energyAvailable - 250
                    count = 3
                    while wiggle_room // 100 >= 1 and count < 50:
                        parts.append(WORK)
                        wiggle_room -= 100
                        count += 1
                    parts.append(MOVE)
                    spawn.createCreep(parts)
                else:
                    creep_name = "{}{}".format("harvester-", Game.time)
                    spawn.spawnCreep([WORK, WORK, CARRY, MOVE], creep_name, {'memory': {'role': 'harvester'}})


module.exports.loop = main
