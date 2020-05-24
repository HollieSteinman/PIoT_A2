import unittest

from AgentPiTester import *

class test_AgentPi(unittest.TestCase):

    def test_unlock(self):

        expectedLocked = "Car unlocked"
        expectedUnlocked = "Car already unlocked"

        actualLocked = unlock(True)
        actualUnlocked = unlock(False)

        self.assertEqual(actualLocked, expectedLocked)
        self.assertEqual(actualUnlocked, expectedUnlocked)

    def test_locked(self):

        expectedUnlocked = "Car locked: Returned" 
        expectedLocked = "Car already locked"

        actualUnlocked = lock(False)
        actualLocked = lock(True)
        
        self.assertEqual(actualLocked, expectedLocked)
        self.assertEqual(actualUnlocked, expectedUnlocked)

    def test_returnCar(self):

        Expected = "Returned"
        Actual = returnCar()

        self.assertEqual(Actual, Expected)

    def test_showMenu(self):

        expectedLockedAndWantsToUnlock = "Car is: locked 1. Unlock 2. Return 3. Set up face recognition Car unlocked"
        expectedLockedAndWantsToReturn = "Car is: locked 1. Unlock 2. Return 3. Set up face recognition Car already locked"
        expectedLockedAndWantsToFR = "Car is: locked 1. Unlock 2. Return 3. Set up face recognition Face Recognition"
        
        expectedUnlockedAndWantsToUnlock = "Car is: unlocked 1. Unlock 2. Return 3. Set up face recognition Car already unlocked"
        expectedUnlockedAndWantsToReturn = "Car is: unlocked 1. Unlock 2. Return 3. Set up face recognition Car locked: Returned"
        expectedUnlockedAndWantsToFR = "Car is: unlocked 1. Unlock 2. Return 3. Set up face recognition Face Recognition"

        actualLockedAndWantsToUnlock = showMenu("1", True)
        actualLockedAndWantsToReturn = showMenu("2", True)
        actualLockedAndWantsToFR = showMenu("3", True)

        actualUnlockedAndWantsToUnlock = showMenu("1", False)
        actualUnlockedAndWantsToReturn = showMenu("2", False)
        actualUnlockedAndWantsToFR = showMenu("3", False)

        self.assertEqual(actualLockedAndWantsToUnlock, expectedLockedAndWantsToUnlock)
        self.assertEqual(actualLockedAndWantsToReturn, expectedLockedAndWantsToReturn)
        self.assertEqual(actualLockedAndWantsToFR, expectedLockedAndWantsToFR)

        self.assertEqual(actualUnlockedAndWantsToUnlock, expectedUnlockedAndWantsToUnlock)
        self.assertEqual(actualUnlockedAndWantsToReturn, expectedUnlockedAndWantsToReturn)
        self.assertEqual(actualUnlockedAndWantsToFR, expectedUnlockedAndWantsToFR)

    def test_showMenu_IncorrectValues(self):
        
        self.assertRaises(ValueError, showMenu, "-1", True)
        self.assertRaises(ValueError, showMenu, "0", False)
        self.assertRaises(ValueError, showMenu, "Hi", True)
        self.assertRaises(ValueError, showMenu, "-20", False)
        self.assertRaises(ValueError, showMenu, "A Car Please", True)
        


if __name__ == '__main__':
    unittest.main()