# 
# Unit Tests for DifferentialSet() Objects
#

import os
import sys
from os.path import abspath, dirname
currdir = dirname(abspath(__file__))+os.sep

import pyomo.modeling
from pyomo.core import *
from pyomo.dae import *
import pyutilib.th as unittest

class TestDifferentialSet(unittest.TestCase):

    # test __init__
    def test_init(self):
        model = ConcreteModel()
        model.t = DifferentialSet(bounds=(0,1))
        del model.t

        model.t = DifferentialSet(initialize=[1,2,3])
        del model.t
    
        model.t = DifferentialSet(bounds=(0,5),initialize=[1,3,5])
        del model.t

        try:
            model.t = DifferentialSet()
            self.fail("Expected ValueError because a DifferentialSet component"/
                      " must contain at least two values upon construction")
        except ValueError:
            pass

    # test bad keyword arguments
    def test_bad_kwds(self):
        model = ConcreteModel()
        try:
            model.t = DifferentialSet(bounds=(0,1),filter=True)
            self.fail("Expected TypeError")
        except TypeError:
            pass
        
        try:
            model.t = DifferentialSet(bounds=(0,1),within=PositiveReals)
            self.fail("Expected TypeError")
        except TypeError:
            pass
        
        try:
            model.t = DifferentialSet(bounds=(0,1),dimen=2)
            self.fail("Expected TypeError")
        except TypeError:
            pass
        
        try:
            model.t = DifferentialSet(bounds=(0,1),virtual=True)
            self.fail("Expected TypeError")
        except TypeError:
            pass

        try:
            model.t = DifferentialSet(bounds=(0,1),validate=True)
            self.fail("Expected TypeError")
        except TypeError:
            pass

    # test valid declarations
    def test_valid_declaration(self):
        model = ConcreteModel()
        model.t = DifferentialSet(bounds=(0,1))
        self.assertTrue(len(model.t)==2)
        self.assertTrue(0 in model.t)
        self.assertTrue(1 in model.t)
        del model.t

        model.t = DifferentialSet(initialize=[1,2,3])
        self.assertTrue(len(model.t)==3)
        self.assertTrue(model.t.first()==1)
        self.assertTrue(model.t.last()==3)
        del model.t
        
        model.t = DifferentialSet(bounds=(0,4),initialize=[1,2,3])
        self.assertTrue(len(model.t)==5)
        self.assertTrue(model.t.first()==0)
        self.assertTrue(model.t.last()==4)
        del model.t

        model.t = DifferentialSet(bounds=(0,4),initialize=[1,2,3,5])
        self.assertTrue(len(model.t)==5)
        self.assertTrue(model.t.first()==0)
        self.assertTrue(model.t.last()==5)
        self.assertTrue(4 not in model.t)
        del model.t

        model.t = DifferentialSet(bounds=(2,6),initialize=[1,2,3,5])
        self.assertTrue(len(model.t)==5)
        self.assertTrue(model.t.first()==1)
        self.assertTrue(model.t.last()==6)
        del model.t

        model.t = DifferentialSet(bounds=(2,4),initialize=[1,3,5])
        self.assertTrue(len(model.t)==3)
        self.assertTrue(2 not in model.t)
        self.assertTrue(4 not in model.t)

    # test invalid declarations
    def test_invalid_declaration(self):
        model = ConcreteModel()
        model.s = Set(initialize=[1,2,3])

        try:
            model.t = DifferentialSet(model.s,bounds=(0,1))
            self.fail("Expected TypeError")
        except TypeError:
            pass

        try:
            model.t = DifferentialSet(bounds=(0,0))
            self.fail("Expected ValueError")
        except ValueError:
            pass

        try:
            model.t = DifferentialSet(initialize=[1])
            self.fail("Expected ValueError")
        except ValueError:
            pass

        try:
            model.t = DifferentialSet(bounds=(None,1))
            self.fail("Expected ValueError")
        except ValueError:
            pass

        try:
            model.t = DifferentialSet(bounds=(0,None))
            self.fail("Expected ValueError")
        except ValueError:
            pass

        try:
            model.t = DifferentialSet(initialize=[(1,2),(3,4)])
            self.fail("Expected ValueError")
        except ValueError:
            pass

        try:
            model.t = DifferentialSet(initialize=['foo','bar'])
            self.fail("Expected ValueError")
        except ValueError:
            pass

    # test the get_changed method
    def test_get_changed(self):
        model = ConcreteModel()
        model.t = DifferentialSet(initialize=[1,2,3])
        self.assertFalse(model.t.get_changed())
        self.assertEqual(model.t._changed,model.t.get_changed())

    # test the set_changed method
    def test_set_changed(self):
        model = ConcreteModel()
        model.t = DifferentialSet(initialize=[1,2,3])
        self.assertFalse(model.t._changed)
        model.t.set_changed(True)
        self.assertTrue(model.t._changed)
        model.t.set_changed(False)
        self.assertFalse(model.t._changed)

        try:
            model.t.set_changed(3)
            self.fail("Expected a ValueError")
        except ValueError:
            pass

class TestIO(unittest.TestCase):
    
    def setUp(self):
        #
        # Create Model
        #
        self.model = AbstractModel()
    
    def tearDown(self):
        if os.path.exists("diffset.dat"):
            os.remove("diffset.dat")

    def test_io1(self):
        OUTPUT=open("diffset.dat","w")
        OUTPUT.write("data;\n")
        OUTPUT.write("set A := 1 3 5 7;\n")
        OUTPUT.write("end;\n")
        OUTPUT.close()
        self.model.A = DifferentialSet()
        self.instance = self.model.create("diffset.dat")
        self.assertEqual( len(self.instance.A), 4 )

    def test_io2(self):
        OUTPUT=open("diffset.dat","w")
        OUTPUT.write("data;\n")
        OUTPUT.write("set A := 1 3 5;\n")
        OUTPUT.write("end;\n")
        OUTPUT.close()
        self.model.A = DifferentialSet(bounds=(0,4))
        self.instance = self.model.create("diffset.dat")
        self.assertEqual( len(self.instance.A), 4)

    def test_io3(self):
        OUTPUT=open("diffset.dat","w")
        OUTPUT.write("data;\n")
        OUTPUT.write("set A := 1 3 5;\n")
        OUTPUT.write("end;\n")
        OUTPUT.close()
        self.model.A = DifferentialSet(bounds=(2,6))
        self.instance = self.model.create("diffset.dat")
        self.assertEqual( len(self.instance.A), 4)

    def test_io4(self):
        OUTPUT=open("diffset.dat","w")
        OUTPUT.write("data;\n")
        OUTPUT.write("set A := 1 3 5;\n")
        OUTPUT.write("end;\n")
        OUTPUT.close()
        self.model.A = DifferentialSet(bounds=(2,4))
        self.instance = self.model.create("diffset.dat")
        self.assertEqual( len(self.instance.A), 3)
    
    def test_io5(self):
        OUTPUT=open("diffset.dat","w")
        OUTPUT.write("data;\n")
        OUTPUT.write("set A := 1 3 5;\n")
        OUTPUT.write("end;\n")
        OUTPUT.close()
        self.model.A = DifferentialSet(bounds=(0,6))
        self.instance = self.model.create("diffset.dat")
        self.assertEqual( len(self.instance.A), 5)

    def test_io6(self):
        OUTPUT=open("diffset.dat","w")
        OUTPUT.write("data;\n")
        OUTPUT.write("set B := 1;\n")
        OUTPUT.write("end;\n")
        OUTPUT.close()
        self.model.B = DifferentialSet()
        try:
            self.instance = self.model.create("diffset.dat")
            self.fail("Expected ValueError because data set has only one value"\
                          " and no bounds are specified")
        except ValueError:
            pass
            
    def test_io7(self):
        OUTPUT=open("diffset.dat","w")
        OUTPUT.write("data;\n")
        OUTPUT.write("set B := 1;\n")
        OUTPUT.write("end;\n")
        OUTPUT.close()
        self.model.B = DifferentialSet(bounds=(0,1))
        self.instance = self.model.create("diffset.dat")
        self.assertEqual( len(self.instance.B), 2)

if __name__ == "__main__":
    unittest.main()
