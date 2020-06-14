import unittest

from AgentPiTester import *

class test_AgentPi(unittest.TestCase):

    def test_unlock_whenLocked(self):

        expectedLocked = "Car unlocked"
        actualLocked = unlock(True)

        self.assertEqual(actualLocked, expectedLocked)

    def test_unlock_whenUnlocked(self):

        expectedUnlocked = "Car already unlocked"
        actualUnlocked = unlock(False)

        self.assertEqual(actualUnlocked, expectedUnlocked)

    def test_locked_whenLocked(self):

        expectedLocked = "Car already locked"
        actualLocked = lock(True)
        
        self.assertEqual(actualLocked, expectedLocked)

    def test_locked_whenUnlocked(self):

        expectedUnlocked = "Car locked: Returned"
        actualUnlocked = lock(False)
        
        self.assertEqual(actualUnlocked, expectedUnlocked)

    def test_returnCar(self):

        Expected = "Returned"
        Actual = returnCar()

        self.assertEqual(Actual, Expected)

    def test_showMenu_whenLocked(self):

        expectedLockedAndWantsToUnlock = "Car is: locked 1. Unlock 2. Return 3. Set up face recognition Car unlocked"
        expectedLockedAndWantsToReturn = "Car is: locked 1. Unlock 2. Return 3. Set up face recognition Car already locked"
        expectedLockedAndWantsToFR = "Car is: locked 1. Unlock 2. Return 3. Set up face recognition Face Recognition"

        actualLockedAndWantsToUnlock = showMenu("1", True)
        actualLockedAndWantsToReturn = showMenu("2", True)
        actualLockedAndWantsToFR = showMenu("3", True)

        self.assertEqual(actualLockedAndWantsToUnlock, expectedLockedAndWantsToUnlock)
        self.assertEqual(actualLockedAndWantsToReturn, expectedLockedAndWantsToReturn)
        self.assertEqual(actualLockedAndWantsToFR, expectedLockedAndWantsToFR)

    def test_showMenu_whenUnlocked(self):
        
        expectedUnlockedAndWantsToUnlock = "Car is: unlocked 1. Unlock 2. Return 3. Set up face recognition Car already unlocked"
        expectedUnlockedAndWantsToReturn = "Car is: unlocked 1. Unlock 2. Return 3. Set up face recognition Car locked: Returned"
        expectedUnlockedAndWantsToFR = "Car is: unlocked 1. Unlock 2. Return 3. Set up face recognition Face Recognition"

        actualUnlockedAndWantsToUnlock = showMenu("1", False)
        actualUnlockedAndWantsToReturn = showMenu("2", False)
        actualUnlockedAndWantsToFR = showMenu("3", False)

        self.assertEqual(actualUnlockedAndWantsToUnlock, expectedUnlockedAndWantsToUnlock)
        self.assertEqual(actualUnlockedAndWantsToReturn, expectedUnlockedAndWantsToReturn)
        self.assertEqual(actualUnlockedAndWantsToFR, expectedUnlockedAndWantsToFR)

    def test_showMenu_IncorrectValues(self):
        
        self.assertRaises(ValueError, showMenu, "-1", True)
        self.assertRaises(ValueError, showMenu, "0", False)
        self.assertRaises(ValueError, showMenu, "Hi", True)
        self.assertRaises(ValueError, showMenu, "-20", False)
        self.assertRaises(ValueError, showMenu, "A Car Please", True)

    def test_engineerMenu_whenLocked(self):

        expectedLockedAndWantsToUnlock = "Car is: locked 1. Unlock/Lock 2. Scan QR code 3. Exit Car unlocked"
        expectedLockedAndWantsToReturn = "Car is: locked 1. Unlock/Lock 2. Scan QR code 3. Exit Recognising QR code..."
        expectedLockedAndWantsToFR = "Car is: locked 1. Unlock/Lock 2. Scan QR code 3. Exit exiting"

        actualLockedAndWantsToUnlock = engineerMenu("1", True)
        actualLockedAndWantsToReturn = engineerMenu("2", True)
        actualLockedAndWantsToFR = engineerMenu("3", True)

        self.assertEqual(actualLockedAndWantsToUnlock, expectedLockedAndWantsToUnlock)
        self.assertEqual(actualLockedAndWantsToReturn, expectedLockedAndWantsToReturn)
        self.assertEqual(actualLockedAndWantsToFR, expectedLockedAndWantsToFR)

    def test_engineerMenu_whenUnlocked(self):

        expectedUnlockedAndWantsToUnlock = "Car is: unlocked 1. Unlock/Lock 2. Scan QR code 3. Exit Car already unlocked"
        expectedUnlockedAndWantsToReturn = "Car is: unlocked 1. Unlock/Lock 2. Scan QR code 3. Exit Recognising QR code..."
        expectedUnlockedAndWantsToFR = "Car is: unlocked 1. Unlock/Lock 2. Scan QR code 3. Exit exiting"

        actualUnlockedAndWantsToUnlock = engineerMenu("1", False)
        actualUnlockedAndWantsToReturn = engineerMenu("2", False)
        actualUnlockedAndWantsToFR = engineerMenu("3", False)

        self.assertEqual(actualUnlockedAndWantsToUnlock, expectedUnlockedAndWantsToUnlock)
        self.assertEqual(actualUnlockedAndWantsToReturn, expectedUnlockedAndWantsToReturn)
        self.assertEqual(actualUnlockedAndWantsToFR, expectedUnlockedAndWantsToFR)

    def test_engineerMenu_IncorrectValues(self):
        
        self.assertRaises(ValueError, engineerMenu, "-1", True)
        self.assertRaises(ValueError, engineerMenu, "0", False)
        self.assertRaises(ValueError, engineerMenu, "Hi", True)
        self.assertRaises(ValueError, engineerMenu, "-20", False)
        self.assertRaises(ValueError, engineerMenu, "A Car Please", True)
        


if __name__ == '__main__':
    unittest.main()