import unittest
import socket

import Agent_Pi.AgentPi as agent

agent.AgentPi.lock

class test_AgentPi(unittest.TestCase):
    
    def setUp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        PORT = 9350
        UNIC_FORMAT = "utf-8"
        BYTES = 1024
        FALSE = '0'
        TRUE = '1'


    def lock(self):
        hi = "hi"
        self.assertEqual(hi, "hi")

if __name__ == '__main__':
    unittest.main()