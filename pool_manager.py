import os
import time


"""
Constant values, including the time to wait between two uses of the same object, and the amount of times an object can be used each day.
"""
class Constants:
    TIME_BETWEEN_USES = 30 * 60 #30 minutes
    USES_PER_DAY = 5

"""
HIGH LEVEL IDEA :
    We want to provide a function, that when called, returns an available item, and if no item is available, signals it.
    It could, in that case, indicate the time to wait before the first item becomes available.
    We could store a list of pairs with the item, and a list of usages, where the time is when this item was last used.
    At each query, we clear the list of usages of usages previous to the current day for performance reasons.
    We iterate through the pair list, and we keep a state of the item which is going to be available the soonest.
    An item is available when the time of the last use + the time to wait between two uses is inferior to the current time, 
    and the item has not been used the maximum amount of times per day.
    Once we find an available item, we update its uses list and we return it. 
    If none is found, we return the computed time left to wait.
"""

def get_day_time(time):
    """
    Returns the number of seconds since the beginning of the day.
    """
    return time % (24 * 60 * 60)

def get_day(time):
    """
    Returns the number of days since the beginning of the epoch.
    """
    return time // (24 * 60 * 60)

def build_object_struct(object_path):
    """
    Builds a dict between filenames in object_path, and their uses list.
    """
    #return list(map(lambda object: (object, []), os.listdir(object_path)))
    dict = {}
    for object in os.listdir(object_path):
        dict[object] = []
    return dict

def print_struct(object_struct):
    """
    Prints the object_struct.
    """
    print('Object struct:')
    for object in object_struct:
        print('{}: {}'.format(object, object_struct[object]))

def get_status(object_struct):
    """
    Returns the first available object in object_struct, and adds the current time to its uses list.
    If no object is available, returns None.
    """
    current_time = time.time()
    current_day = get_day(current_time)
    current_day_time = get_day_time(current_time)

    least_used_available_object = None
    least_uses = None
    soonest_time_left = None


    for object in object_struct:
        uses = object_struct[object]

        # We clear the uses list of uses previous to the current day.
        uses = list(filter(lambda use: get_day(use) == current_day, uses))
        object_struct[object] = uses

        # We check if the object is available and if it is the least used object yet.
        if len(uses) < Constants.USES_PER_DAY: 
            if (len(uses) == 0 or uses[-1] + Constants.TIME_BETWEEN_USES < current_time) and (least_used_available_object is None or len(uses) < least_uses): #meaning that this object is the least used object yet
                # If it is, we update our state
                least_used_available_object = object
                least_uses = len(uses)

            # If this object still has uses left for today, we check if it is going to be available the soonest, but only if we haven't found an available object yet.
            elif least_used_available_object is None:
                time_left = uses[-1] + Constants.TIME_BETWEEN_USES - current_time
                # We keep the object which is going to be available the soonest.
                if soonest_time_left is None or time_left < soonest_time_left:
                    soonest_time_left = time_left

    # At the end of the for loop, least_used_available_object is either None, or the least used available object,
    # and soonest_time_left is either None, or the time left to wait for the soonest object to be available.
    
    if least_used_available_object is not None:
        #object_struct[least_used_available_object].append(current_time)
        return least_used_available_object, None
    elif soonest_time_left is not None:
        return None, soonest_time_left
    else:
        #no object is available for today
        return None, None
    

def use_object(object_struct, object):
    """
    Adds the current time to the uses list of object.
    """
    object_struct[object].append(time.time())