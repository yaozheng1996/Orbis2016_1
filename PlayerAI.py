from PythonClientAPI.libs.Game import PointUtils
from PythonClientAPI.libs.Game.Enums import *
from PythonClientAPI.libs.Game.Entities import *
from PythonClientAPI.libs.Game.World import *


class PlayerAI:
    def __init__(self):
        pass


    def do_move(self, world, enemy_units, friendly_units):
        """
        This method will get called every turn; Your glorious AI code goes here.

        :param World world: The latest state of the world.
        :param list[EnemyUnit] enemy_units: An array of all 4 units on the enemy team. Their order won't change.
        :param list[FriendlyUnit] friendly_units: An array of all 4 units on your team. Their order won't change.
        """
        for i in world.control_points:
            print(i.is_mainframe)
            print(i.controlling_team)

        for i in range(0, 4):
            shot = False
            if (friendly_units[i].check_pickup_result()==PickupResult.UNIT_DEAD):
                continue
            if (friendly_units[i].check_pickup_result()==PickupResult.PICK_UP_VALID):
                friendly_units[i].pickup_item_at_position()
                continue
            if (friendly_units[i].check_shield_activation()==ActivateShieldResult.SHIELD_ACTIVATION_VALID):
                friendly_units[i].activated_shield()
                continue
            for j in range(0,4):
                if (friendly_units[i].check_shot_against_enemy(enemy_units[j]) == ShotResult.CAN_HIT_ENEMY):
                    friendly_units[i].shoot_at(enemy_units[j])
                    shot = True
                    break

            if (shot!= True):
                prior = self.priorityList(world,friendly_units[i])

                friendly_units[i].move_to_destination(prior)

        # while friendly_units[i].prior[0] in used_list & prior not empty
                #prior = prior[1:]

    def priorityList(self, world, friendly_unit):
        #Priority Factor Index
        RIFLE = 0.9
        SNIPER = 0.7
        SCATTER = 0.6
        SHIELD = 0.8
        REPAIR = 0.1
        FRAME_ENEMY = 1
        FRAME_FRIEND = 0.7
        FRAME_NEUTRAL = 0.8
        FLAG_ENEMY = 0.8
        FLAG_FRIEND = 0.6
        FLAG_NEUTRAL = 0.4

        # Priority function returns a list of coordinates, with the first being the closest highest priority item
        rifle_positions = world.get_positions_of_pickup_type(PickupType.WEAPON_LASER_RIFLE)
        sniper_positions = world.get_positions_of_pickup_type(PickupType.WEAPON_RAIL_GUN)
        scatter_positions = world.get_positions_of_pickup_type(PickupType.WEAPON_SCATTER_GUN)
        shield_positions = world.get_positions_of_pickup_type(PickupType.SHIELD)
        repair_positions = world.get_positions_of_pickup_type(PickupType.REPAIR_KIT)
        frame_positions = []
        flag_positions = []
        for i in world.control_points:
            print(i.is_mainframe)
            print(i.controlling_team)
            if i.is_mainframe == True:
                frame_positions.append(i.position)
            else:
                flag_positions.append(i.position)

        priorList = []

        for i in rifle_positions:
            distance = (chebyshev_distance(friendly_unit.position, i))
            priorList.append([i[0], i[1],distance*RIFLE])
        for i in sniper_positions:
            distance = (chebyshev_distance(friendly_unit.position, i))
            priorList.append([i[0], i[1], distance*SNIPER])
        for i in scatter_positions:
            distance = (chebyshev_distance(friendly_unit.position, i))
            priorList.append([i[0], i[1], distance*SCATTER])
        for i in shield_positions:
            distance = (chebyshev_distance(friendly_unit.position, i))
            priorList.append([i[0], i[1], distance*SHIELD])
        for i in repair_positions:
            distance = (chebyshev_distance(friendly_unit.position, i))
            priorList.append([i[0], i[1], distance*REPAIR])
        for i in world.control_points:
            distance = (chebyshev_distance(friendly_unit.position, i.position))
            if i.is_mainframe==True:
                if (i.controlling_team == Team.AMBER):
                    priorList.append([i.position[0], i.position[1], distance * FRAME_ENEMY])
                elif (i.controlling_team == Team.BLUE):
                    priorList.append([i.position[0], i.position[1], distance * FRAME_FRIEND])
                else:
                    priorList.append([i.position[0], i.position[1], distance * FRAME_NEUTRAL])
            else:
                if (i.controlling_team == Team.AMBER):
                    priorList.append([i.position[0], i.position[1], distance * FLAG_ENEMY])
                elif (i.controlling_team == Team.BLUE):
                    priorList.append([i.position[0], i.position[1], distance * FLAG_FRIEND])
                else:
                    priorList.append([i.position[0], i.position[1], distance * FLAG_NEUTRAL])
        print(priorList)

        # Sort priorList by [][2]
        #

        alist = rifle_positions + sniper_positions + scatter_positions + shield_positions + repair_positions + frame_positions + flag_positions
        priorList = []
        #for i in alist:
         #   distance = (chebyshev_distance(friendly_unit.position, i))
         #   priorList.append(i.append(distance*))
        if (alist):
            return alist[0]
        return ()







#-----------------------------------------------------------------------------------------------------------------------
    def quickSort(alist):
        quickSortHelper(alist, 0, len(alist) - 1)

    def quickSortHelper(alist, first, last):
        if first < last:
            splitpoint = partition(alist, first, last)

            quickSortHelper(alist, first, splitpoint - 1)
            quickSortHelper(alist, splitpoint + 1, last)

    def partition(alist, first, last):
        pivotvalue = alist[first]

        leftmark = first + 1
        rightmark = last

        done = False
        while not done:

            while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
                leftmark = leftmark + 1

            while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
                rightmark = rightmark - 1

            if rightmark < leftmark:
                done = True
            else:
                temp = alist[leftmark]
                alist[leftmark] = alist[rightmark]
                alist[rightmark] = temp

        temp = alist[first]
        alist[first] = alist[rightmark]
        alist[rightmark] = temp

        return rightmark
