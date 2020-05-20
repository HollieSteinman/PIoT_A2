import unittest
import socket

from Agent_Pi import AgentPi

class test_AgentPi(unittest.TestCase):

    # def setUp(self):
    #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     PORT = 9350
    #     UNIC_FORMAT = "utf-8"
    #     BYTES = 1024
    #     FALSE = '0'
    #     TRUE = '1'

    def being_Locked(self):
        hi = 1
        self.assertEqual(hi, 1)

if __name__ == '__main__':
    unittest.main()