'''
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
    '''

'''sources = creep.room.find(FIND_SOURCES)
def temp(s):
    return creep.pos.getRangeTo(s)
nearest = _.sortBy(sources, temp)'''

'''sources = creep.room.find(FIND_SOURCES)
def temp(s):
    return creep.pos.getRangeTo(s)
nearest = _.sortBy(sources, temp)'''

'''
sources = creep.room.find(FIND_SOURCES)
if creep.harvest(sources[0]) == ERR_NOT_IN_RANGE:
    creep.moveTo(sources[0], {"visualizePathStyle": {"stroke": '#ffaa00'}})
'''

'''
targets = creep.room.find(FIND_CONSTRUCTION_SITES)
if targets.length:
    if creep.build(targets[0]) == ERR_NOT_IN_RANGE:
        creep.moveTo(targets[0], {"visualizePathStyle": {"stroke": '#ffffff'}})
'''

