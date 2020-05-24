# Class that implements similar method to that of the Agent Pi class for testing

def returnCar():
    return "Returned"

def unlock(locked):
    if(locked == True):
        return "Car unlocked"
    else:
        return "Car already unlocked"
    
def lock(locked):
    if(locked == False):
        return "Car locked: " + returnCar()
    else:
        return "Car already locked"

def showMenu(input, locked):
    
    if(input.isdigit()):
        newInput = int(input)
        if(newInput > 3 or newInput < 1):
            raise ValueError("Please enter an input between 1 and 3")

    else:
        raise ValueError("Please enter a number")
    
    string = ""
    
    lock_status = ""
    
    if locked:
        lock_status = "locked"
    else:
        lock_status = "unlocked"
    
    string += "Car is: " + lock_status + " 1. Unlock 2. Return 3. Set up face recognition "

    if(newInput == 1):
        string += unlock(locked)
    if(newInput == 2):
        string += lock(locked)
    if(newInput == 3):
        # face recognition method
        string += "Face Recognition"

    return string
