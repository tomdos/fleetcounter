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
        self.assertRaises(ValueError, self.fc.sanityN, '')
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
    #def setUp(self):
    #    self.input = (
    #        "id1,m1,4,0,0,0,0",
    #        "id2,m1,4,0,1,1,1",
    #        "id3,m1,4,1,1,1,1"
    #    )


    def test_FleetCounter_ok(self):
        input = [
            "id1,m1,4,0,0,0,0"
        ]

        fc = fleetcounter.FleetCounter(input)
        fc.printEmpty()
        self.assertEqual(fc.getStrEmpty(), "EMPTY: M1=1; M2=0; M3=0;")
        self.assertEqual(fc.getStrFull(), "FULL: M1=1; M2=0; M3=0;")
        self.assertEqual(fc.getStrMostFilled(), "MOST FILLED: M1=1,1; M2=0,0; M3=0,0;")



if __name__ == "__main__":
    unittest.main()
