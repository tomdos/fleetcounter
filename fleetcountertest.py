#!/usr/bin/env  python3

import unittest
import fleetcounter


class FleetCounterTest(unittest.TestCase):
    def setUp(self):
        self.fc = fleetcounter.FleetCounter(None)

    def init_lineStats(self):
        self.host = 'id'
        self.instance = 'M1'
        self.n = 4

    def test_lineStats_empty_count(self):
        self.init_lineStats()
        slots = (0,0,0,0)

        self.assertEqual(self.fc.getStrEmpty(), "EMPTY: M1=0; M2=0; M3=0;")
        self.fc.lineStats(self.host, self.instance, self.n, slots)
        self.assertEqual(self.fc.getStrEmpty(), "EMPTY: M1=1; M2=0; M3=0;")
        self.fc.lineStats(self.host, self.instance, self.n, slots)
        self.assertEqual(self.fc.getStrEmpty(), "EMPTY: M1=2; M2=0; M3=0;")

    def test_lineStats_full_count(self):
        self.init_lineStats()
        slots = (1,1,1,1)

        self.assertEqual(self.fc.getStrFull(), "FULL: M1=0; M2=0; M3=0;")
        self.fc.lineStats(self.host, self.instance, self.n, slots)
        self.assertEqual(self.fc.getStrFull(), "FULL: M1=1; M2=0; M3=0;")
        self.fc.lineStats(self.host, self.instance, self.n, slots)
        self.assertEqual(self.fc.getStrFull(), "FULL: M1=2; M2=0; M3=0;")

    def test_lineStats_mostFilled_count(self):
        self.init_lineStats()
        slots = (0,0,1,1)

        self.assertEqual(self.fc.getStrMostFilled(), "MOST FILLED: M1=0,0; M2=0,0; M3=0,0;")
        self.fc.lineStats(self.host, self.instance, self.n, slots)
        self.assertEqual(self.fc.getStrMostFilled(), "MOST FILLED: M1=1,2; M2=0,0; M3=0,0;")
        self.fc.lineStats(self.host, self.instance, self.n, slots)
        self.assertEqual(self.fc.getStrMostFilled(), "MOST FILLED: M1=2,2; M2=0,0; M3=0,0;")

        slots = (0,1,1,1)
        self.fc.lineStats(self.host, self.instance, self.n, slots)
        self.assertEqual(self.fc.getStrMostFilled(), "MOST FILLED: M1=1,1; M2=0,0; M3=0,0;")

    def test_sanityHost(self):
        self.assertRaises(RuntimeError, self.fc.sanityHost, '')
        self.assertEqual(self.fc.sanityHost("myHost"), "myHost")

    def test_sanityInstance_upper(self):
        self.assertEqual(self.fc.sanityInstance("m1"), "M1")
        self.assertRaises(AttributeError, self.fc.sanityInstance, 1)

    def test_sanityInstance_dictKey(self):
        self.assertEqual(self.fc.sanityInstance("m1"), "M1")
        self.assertEqual(self.fc.sanityInstance("m2"), "M2")
        self.assertEqual(self.fc.sanityInstance("m3"), "M3")
        self.assertRaises(KeyError, self.fc.sanityInstance, 'Mx')

    def test_sanityN(self):
        self.assertEqual(self.fc.sanityN(1), 1)
        self.assertRaises(ValueError, self.fc.sanityN, 'N')
        self.assertRaises(RuntimeError, self.fc.sanityN, '')
        self.assertRaises(TypeError, self.fc.sanityN, [])

    def test_sanitySlots_len(self):
        self.assertRaises(RuntimeError, self.fc.sanitySlots, 2,'1,0,1')

    def test_sanitySlots_transform(self):
        self.assertEqual(self.fc.sanitySlots(3, '1,0,1'), (1,0,1))
        self.assertRaises(RuntimeError, self.fc.sanitySlots, 2,'1,2')

    def test_processLine(self):
        self.assertRaises(ValueError, self.fc.processLine, "i1")
        self.assertRaises(ValueError, self.fc.processLine, "i1,i2")
        self.assertRaises(ValueError, self.fc.processLine, "i1,i2,i3")

    def test_process(self):
        self.fc.input = 1
        self.assertRaises(TypeError, self.fc.process)
        self.fc.input = (1,)
        self.assertRaises(AttributeError, self.fc.process)

    def test_getStrEmpty(self):
        self.assertEqual(self.fc.getStrEmpty(), "EMPTY: M1=0; M2=0; M3=0;")

    def test_getStrFull(self):
        self.assertEqual(self.fc.getStrFull(), "FULL: M1=0; M2=0; M3=0;")

    def test_getStrMostFilled(self):
        self.assertEqual(self.fc.getStrMostFilled(), "MOST FILLED: M1=0,0; M2=0,0; M3=0,0;")



class FleetCounterMockTest(unittest.TestCase):
    def test_FleetCounter_ok_full_empty(self):
        '''Simple Full/Empty check with instance name check.'''
        input = (
            "id,m1,4,0,0,0,0",
            "id,m2,4,0,0,0,0",
            "id,m3,4,0,0,0,0",
            "id,m3,4,0,0,0,0",
            "id,m3,4,0,0,0,0",
            "id,M1,4,1,1,1,1",
            "id,M2,4,1,1,1,1",
            "id,M3,4,1,1,1,1",
            "id,M3,4,1,1,1,1",
            "id,M3,4,1,1,1,1",
        )
        
        fc = fleetcounter.FleetCounter(input)
        fc.process()
        self.assertEqual(fc.getStrEmpty(), "EMPTY: M1=1; M2=1; M3=3;")
        self.assertEqual(fc.getStrFull(), "FULL: M1=1; M2=1; M3=3;")
        self.assertEqual(fc.getStrMostFilled(), "MOST FILLED: M1=0,0; M2=0,0; M3=0,0;")


    def test_FleetCounter_ok_half(self):
        '''Half empty and half full. One slot test.'''
        input = (
            "id,m1,1,0",
            "id,m2,1,1",
            "id,m3,2,0,0",
            "id,m3,2,1,1",
            "id,m3,2,0,1"
        )
        
        fc = fleetcounter.FleetCounter(input)
        fc.process()
        self.assertEqual(fc.getStrEmpty(), "EMPTY: M1=1; M2=0; M3=1;")
        self.assertEqual(fc.getStrFull(), "FULL: M1=0; M2=1; M3=1;")
        self.assertEqual(fc.getStrMostFilled(), "MOST FILLED: M1=0,0; M2=0,0; M3=1,1;")
         

    def test_FleetCounter_ok_most(self):
        '''Most filed test - increase number of slots.'''
        input = (
            "id,m1,4,0,1,1,1",
            "id,m1,5,0,1,1,1,1",
            "id,m1,6,0,1,1,1,1,1",
            "id,m1,7,0,1,1,1,1,1,1",
            "id,m2,6,0,0,0,0,0,1",
            "id,m3,6,0,0,0,0,0,1",
            "id,m3,6,0,0,0,0,0,1"
        )
        
        fc = fleetcounter.FleetCounter(input)
        fc.process()
        self.assertEqual(fc.getStrEmpty(), "EMPTY: M1=0; M2=0; M3=0;")
        self.assertEqual(fc.getStrFull(), "FULL: M1=0; M2=0; M3=0;")
        self.assertEqual(fc.getStrMostFilled(), "MOST FILLED: M1=4,1; M2=1,5; M3=2,5;")
        
        
    def test_FleetCounter_not_id(self):    
        '''Missing identifier'''
        input = (",m1,4,1,1,1,1",)
        fc = fleetcounter.FleetCounter(input)
        self.assertRaisesRegex(RuntimeError, "No host id.", fc.process)
        
        
    def test_FleetCounter_not_instance(self):
        '''Missing instance name'''
        input = ("id,,4,1,1,1,1",)
        fc = fleetcounter.FleetCounter(input)
        self.assertRaises(KeyError, fc.process)
        
        
    def test_FleetCounter_wrong_instance(self):
        '''Wrong instance name'''
        input = ("id,1,4,1,1,1,1",)
        fc = fleetcounter.FleetCounter(input)
        self.assertRaises(KeyError, fc.process)
        
        input = ("id,XXX,4,1,1,1,1",)
        fc = fleetcounter.FleetCounter(input)
        self.assertRaises(KeyError, fc.process)
        
        
    def test_FleetCounter_wrong_slots_number(self):
        '''Number of slots and N is different.'''
        input = ("id,m1,,1,1,1,1",)        
        fc = fleetcounter.FleetCounter(input)
        self.assertRaises(RuntimeError, fc.process)
        
        input = ("id,m1,,1,1,1,1",)
        fc = fleetcounter.FleetCounter(input)
        self.assertRaises(RuntimeError, fc.process)           
        
        
    def test_FleetCounter_wrong_slots_values(self):
        '''Different value than 0/1'''
        input = ("id,m1,4,1,2,1,1",)        
        fc = fleetcounter.FleetCounter(input)
        self.assertRaises(RuntimeError, fc.process)
        
        input = ("id,m1,4,,1,1,1",)
        fc = fleetcounter.FleetCounter(input)
        self.assertRaises(RuntimeError, fc.process)
        

    def test_FleetCounter_wrong_input(self):    
        input = ("",)        
        fc = fleetcounter.FleetCounter(input)
        self.assertRaises(ValueError, fc.process)
        
        input = (",",)        
        fc = fleetcounter.FleetCounter(input)
        self.assertRaises(ValueError, fc.process)     
        
        # parsing is processed but no host found..
        input = (",,,",)        
        fc = fleetcounter.FleetCounter(input)
        self.assertRaises(RuntimeError, fc.process)              


if __name__ == "__main__":
    unittest.main()
    
