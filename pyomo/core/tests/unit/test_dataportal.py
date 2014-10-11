#
# Unit Tests for DataPortal objects
#

import os
import sys
from os.path import abspath, dirname
pyomo_dir=dirname(dirname(abspath(__file__)))+os.sep+".."+os.sep+".."

import pyutilib.common
import pyutilib.th as unittest
from pyomo.core import *
import pyomo
from pyomo.core.base.plugin import DataManagerFactory
import pyomo.modeling

try:
    import yaml
    yaml_available=True
except ImportError:
    yaml_available=False

currdir=dirname(abspath(__file__))+os.sep
example_dir=pyomo_dir+os.sep+".."+os.sep+"examples"+os.sep+"pyomo"+os.sep+"tutorials"+os.sep+"tab"+os.sep
tutorial_dir=pyomo_dir+os.sep+".."+os.sep+"examples"+os.sep+"pyomo"+os.sep+"tutorials"+os.sep

try:
    xls_interface = DataManagerFactory('xls').available()
except:
    xls_interface = False
try:
    xlsx_interface = DataManagerFactory('xlsx').available()
except:
    xlsx_interface = False
try:
    xlsb_interface = DataManagerFactory('xlsb').available()
except:
    xlsb_interface = False
try:
    xlsm_interface = DataManagerFactory('xlsm').available()
except:
    xlsm_interface = False
try:
    yaml_interface = DataManagerFactory('yaml').available()
except:
    yaml_interface = False



@unittest.skipIf(not xls_interface, "No XLS interface available")
class PyomoTableData(unittest.TestCase):

    def setUp(self):
        pass

    def construct(self,filename):
        pass

    def test_read_set(self):
        td = DataManagerFactory('xls')
        td.initialize(filename=currdir+"Book1.xls", range="TheRange", format='set', set="X")
        try:
            td.open()
            td.read()
            td.close()
            self.assertEqual( td._info, ['set', 'X', ':=', 'A1', 2.0, 3.0, 4.0, 'A5', 6.0, 7.0, 8.0, 'A9', 10.0, 11.0, 12.0, 'A13', 14.0, 15.0, 16.0])
        except pyutilib.common.ApplicationError:
            pass

    def test_read_param1(self):
        td = DataManagerFactory('xls')
        td.initialize(filename=currdir+"Book1.xls", range="TheRange", index=['aa'], param=['bb','cc','dd'])
        try:
            td.open()
            td.read()
            td.close()
            self.assertEqual( td._info, ['param', ':', 'bb', 'cc', 'dd', ':=', 'A1', 2.0, 3.0, 4.0, 'A5', 6.0, 7.0, 8.0, 'A9', 10.0, 11.0, 12.0, 'A13', 14.0, 15.0, 16.0])
        except pyutilib.common.ApplicationError:
            pass

    def test_read_param2(self):
        td = DataManagerFactory('xls')
        td.initialize(filename=currdir+"Book1.xls",range="TheRange", index_name="X", index=['aa'], param=['bb','cc','dd'])
        try:
            td.open()
            td.read()
            td.close()
            self.assertEqual( td._info, ['param', ':', 'X', ':', 'bb', 'cc', 'dd', ':=', 'A1', 2.0, 3.0, 4.0, 'A5', 6.0, 7.0, 8.0, 'A9', 10.0, 11.0, 12.0, 'A13', 14.0, 15.0, 16.0])
        except pyutilib.common.ApplicationError:
            pass

    def test_read_param3(self):
        td = DataManagerFactory('xls')
        td.initialize(filename=currdir+"Book1.xls",range="TheRange", index_name="X", index=['aa','bb','cc'], param=["dd"], param_name={'dd':'a'})
        try:
            td.open()
            td.read()
            td.close()
            self.assertEqual( td._info, ['param', ':', 'X', ':', 'a', ':=', 'A1', 2.0, 3.0, 4.0, 'A5', 6.0, 7.0, 8.0, 'A9', 10.0, 11.0, 12.0, 'A13', 14.0, 15.0, 16.0])
        except pyutilib.common.ApplicationError:
            pass

    def test_read_param4(self):
        td = DataManagerFactory('xls')
        td.initialize(filename=currdir+"Book1.xls",range="TheRange", index_name="X", index=['aa','bb'], param=['cc','dd'], param_name={'cc':'a', 'dd':'b'})
        try:
            td.open()
            td.read()
            td.close()
            self.assertEqual( td._info, ['param', ':', 'X', ':', 'a', 'b', ':=', 'A1', 2.0, 3.0, 4.0, 'A5', 6.0, 7.0, 8.0, 'A9', 10.0, 11.0, 12.0, 'A13', 14.0, 15.0, 16.0])
        except pyutilib.common.ApplicationError:
            pass

    def test_read_array1(self):
        td = DataManagerFactory('xls')
        td.initialize(filename=currdir+"Book1.xls",range="TheRange", param="X", format="array")
        try:
            td.open()
            td.read()
            td.close()
            self.assertEqual( td._info, ['param', 'X', ':', 'bb', 'cc', 'dd', ':=', 'A1', 2.0, 3.0, 4.0, 'A5', 6.0, 7.0, 8.0, 'A9', 10.0, 11.0, 12.0, 'A13', 14.0, 15.0, 16.0])
        except pyutilib.common.ApplicationError:
            pass

    def test_read_array2(self):
        td = DataManagerFactory('xls')
        td.initialize(filename=currdir+"Book1.xls",range="TheRange",param="X",format="transposed_array")
        try:
            td.open()
            td.read()
            td.close()
            self.assertEqual( td._info, ['param', 'X', '(tr)',':', 'bb', 'cc', 'dd', ':=', 'A1', 2.0, 3.0, 4.0, 'A5', 6.0, 7.0, 8.0, 'A9', 10.0, 11.0, 12.0, 'A13', 14.0, 15.0, 16.0])
        except pyutilib.common.ApplicationError:
            pass

    def test_error1(self):
        td = DataManagerFactory('xls')
        td.initialize(filename="bad")
        try:
            td.open()
            self.fail("Expected IOError because of bad file")
        except IOError:
            pass

    def test_error2(self):
        td = DataManagerFactory('xls')
        try:
            td.open()
            self.fail("Expected IOError because no file specified")
        except (IOError,AttributeError):
            pass

    def test_error3(self):
        td = DataManagerFactory('txt')
        try:
            td.initialize(filename=currdir+"display.txt")
            td.open()
            self.fail("Expected IOError because of bad file type")
        except (IOError, AttributeError):
            pass

    def test_error4(self):
        td = DataManagerFactory('txt')
        try:
            td.initialize(filename=currdir+"dummy")
            td.open()
            self.fail("Expected IOError because of bad file type")
        except (IOError, AttributeError):
            pass

    def test_error5(self):
        td = DataManagerFactory('tab')
        td.initialize(filename=example_dir+"D.tab", param="D", format="foo")
        td.open()
        try:
            td.read()
            self.fail("Expected IOError because of bad format")
        except ValueError:
            pass


class PyomoDataPortal(unittest.TestCase):

    def test_tableA1_1(self):
        # Importing a single column of data
        model=AbstractModel()
        model.A = Set()
        data = DataPortal(filename=os.path.abspath(example_dir+'A.tab'), set=model.A)
        instance = model.create(data)
        self.assertEqual(instance.A.data(), set(['A1', 'A2', 'A3']))

    def test_tableA1_2(self):
        # Importing a single column of data
        model=AbstractModel()
        model.A = Set()
        data = DataPortal()
        data.load(filename=os.path.abspath(example_dir+'A.tab'), set=model.A)
        instance = model.create(data)
        self.assertEqual(instance.A.data(), set(['A1', 'A2', 'A3']))

    def test_tableA1_3(self):
        # Importing a single column of data
        model=AbstractModel()
        model.A = Set()
        data = DataPortal()
        data.connect(filename=os.path.abspath(example_dir+'A.tab'))
        data.load(set=model.A)
        data.disconnect()
        instance = model.create(data)
        self.assertEqual(instance.A.data(), set(['A1', 'A2', 'A3']))

    def test_md1(self):
        md = DataPortal()
        md.connect(filename=example_dir+"A.tab")
        try:
            md.load()
            self.fail("Must specify a model")
        except ValueError:
            pass
        model=AbstractModel()
        try:
            md.load(model=model)
            self.fail("Expected ValueError")
        except ValueError:
            pass
        model.A=Set()

    def test_md2(self):
        md = DataPortal()
        model=AbstractModel()
        model.A=Set()
        md.load(model=model, filename=currdir+"data1.dat")

    def test_md3(self):
        md = DataPortal()
        model=AbstractModel()
        model.A=Set()
        try:
            md.load(model=model, filename=currdir+"data2.dat")
            self.fail("Expected error because of extraneous text")
        except IOError:
            pass

    def test_md4(self):
        md = DataPortal()
        model=AbstractModel()
        model.A=Set()
        model.B=Set()
        model.C=Set()
        md.load(model=model, filename=currdir+"data3.dat")

    def test_md5(self):
        md = DataPortal()
        model=AbstractModel()
        model.A=Set()
        try:
            md.load(model=model, filename=currdir+"data4.dat")
        except (ValueError,IOError):
            pass

    def test_md6(self):
        md = DataPortal()
        model=AbstractModel()
        model.A=Set()
        try:
            md.load(model=model, filename=currdir+"data5.dat")
        except ValueError:
            pass

    def test_md7(self):
        md = DataPortal()
        model=AbstractModel()
        try:
            md.load(model=model, filename=currdir+"data1.tab")
            self.fail("Expected IOError")
        except IOError:
            pass

    def test_md8(self):
        md = DataPortal()
        model=AbstractModel()
        model.A=Set()
        try:
            md.load(model=model, filename=currdir+"data6.dat")
            self.fail("Expected IOError")
        except IOError:
            pass

    def test_md9(self):
        md = DataPortal()
        model=AbstractModel()
        model.A=Set()
        model.B=Param(model.A)
        md.load(model=model, filename=currdir+"data7.dat")

    def test_md10(self):
        md = DataPortal()
        model=AbstractModel()
        model.A=Param(within=Boolean)
        model.B=Param(within=Boolean)
        model.Z=Set()
        md.load(model=model, filename=currdir+"data8.dat")
        instance = model.create(md)

    def test_md11(self):
        cwd = os.getcwd()
        os.chdir(currdir)
        md = DataPortal()
        model=AbstractModel()
        model.A=Set()
        model.B=Set()
        model.C=Set()
        model.D=Set()
        md.load(model=model, filename=currdir+"data11.dat")
        os.chdir(cwd)

    def test_md11(self):
        cwd = os.getcwd()
        os.chdir(currdir)
        model=AbstractModel()
        model.a=Param()
        model.b=Param()
        model.c=Param()
        model.d=Param()
        # Test 1
        instance = model.create(currdir+'data14.dat', namespaces=['ns1','ns2'])
        self.assertEqual( value(instance.a), 1)
        self.assertEqual( value(instance.b), 2)
        self.assertEqual( value(instance.c), 2)
        self.assertEqual( value(instance.d), 2)
        # Test 2
        instance = model.create(currdir+'data14.dat', namespaces=['ns1','ns3','nsX'])
        self.assertEqual( value(instance.a), 1)
        self.assertEqual( value(instance.b), 100)
        self.assertEqual( value(instance.c), 3)
        self.assertEqual( value(instance.d), 100)
        # Test None
        instance = model.create(currdir+'data14.dat')
        self.assertEqual( value(instance.a), -1)
        self.assertEqual( value(instance.b), -2)
        self.assertEqual( value(instance.c), -3)
        self.assertEqual( value(instance.d), -4)
        #
        os.chdir(cwd)

    def test_md12(self):
        model = ConcreteModel()
        model.A = Set()
        md = DataPortal()
        try:
            md.load(filename=example_dir+'A.tab', format='bad', set=model.A)
            self.fail("Bad format error")
        except ValueError:
            pass
        try:
            md.load(filename=example_dir+'A.tab')
            self.fail("Bad format error")
        except ValueError:
            pass


class TestOnlyTextPortal(unittest.TestCase):

    suffix = '.tab'
    skiplist = []

    def check_skiplist(self, name):
        if name in self.skiplist:
            self.skipTest('Skipping test %s' % name)

    def create_options(self, name):
        return {'filename':os.path.abspath(tutorial_dir+os.sep+'tab'+os.sep+name+self.suffix)}

    def create_write_options(self, name):
        return {'filename':os.path.abspath(currdir+os.sep+name+self.suffix)}

    def test_tableA(self):
        # Importing an unordered set of arbitrary data
        self.check_skiplist('tableA')
        dp = DataPortal()
        dp.load(set='A', **self.create_options('A'))
        self.assertEqual(set(dp.data('A')), set(['A1', 'A2', 'A3']))

    def test_tableB(self):
        # Importing an unordered set of numeric data
        self.check_skiplist('tableB')
        dp = DataPortal()
        dp.load(set='B', **self.create_options('B'))
        self.assertEqual(set(dp.data('B')), set([1, 2, 3]))

    def test_tableC(self):
        # Importing a multi-column table, where all columns are
        # treated as values for a set with tuple values.
        self.check_skiplist('tableC')
        dp = DataPortal()
        dp.load(set='C', **self.create_options('C'))
        self.assertEqual(set(dp.data('C')), set([('A1',1), ('A1',2), ('A1',3), ('A2',1), ('A2',2), ('A2',3), ('A3',1), ('A3',2), ('A3',3)]))

    def test_tableD(self):
        # Importing a 2D array of data as a set.
        self.check_skiplist('tableD')
        dp = DataPortal()
        dp.load(set='D', format='set_array', **self.create_options('D'))
        self.assertEqual(set(dp.data('D')), set([('A1',1), ('A2',2), ('A3',3)]))

    def test_tableZ(self):
        # Importing a single parameter
        self.check_skiplist('tableZ')
        dp = DataPortal()
        dp.load(param='Z', **self.create_options('Z'))
        self.assertEqual(dp.data('Z'), 1.1)

    def test_tableY(self):
        # Same as tableXW.
        self.check_skiplist('tableY')
        dp = DataPortal()
        dp.load(param='Y', **self.create_options('Y'))
        self.assertEqual(dp.data('Y'), {'A1':3.3,'A2':3.4,'A3':3.5})

    def test_tableXW_1(self):
        # Importing a table, but only reporting the values for the non-index
        # parameter columns.  The first column is assumed to represent an
        # index column.
        self.check_skiplist('tableXW_1')
        dp = DataPortal()
        dp.load(param=('X', 'W'), **self.create_options('XW'))
        self.assertEqual(dp.data('X'), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(dp.data('W'), {'A1':4.3,'A2':4.4,'A3':4.5})

    def test_tableXW_3(self):
        # Like test_tableXW_1, except that set A is defined in the import statment.
        self.check_skiplist('tableXW_3')
        dp = DataPortal()
        dp.load(index='A', param=('X', 'W'), **self.create_options('XW'))
        self.assertEqual(set(dp.data('A')), set(['A1','A2','A3']))
        self.assertEqual(dp.data('X'), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(dp.data('W'), {'A1':4.3,'A2':4.4,'A3':4.5})

    def test_tableXW_4(self):
        # Like test_tableXW_1, except that set A is defined in the import statment and all values are mapped.
        self.check_skiplist('tableXW_4')
        dp = DataPortal()
        dp.load(select=('A', 'W', 'X'), index='B', param=('R', 'S'), **self.create_options('XW'))
        self.assertEqual(set(dp.data('B')), set(['A1','A2','A3']))
        self.assertEqual(dp.data('S'), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(dp.data('R'), {'A1':4.3,'A2':4.4,'A3':4.5})

    def test_tableT(self):
        # Importing a 2D array of parameters that are transposed.
        self.check_skiplist('tableT')
        dp = DataPortal()
        dp.load(format='transposed_array', param='T', **self.create_options('T'))
        self.assertEqual(dp.data('T'), {('A2', 'I1'): 2.3, ('A1', 'I2'): 1.4, ('A1', 'I3'): 1.5, ('A1', 'I4'): 1.6, ('A1', 'I1'): 1.3, ('A3', 'I4'): 3.6, ('A2', 'I4'): 2.6, ('A3', 'I1'): 3.3, ('A2', 'I3'): 2.5, ('A3', 'I2'): 3.4, ('A2', 'I2'): 2.4, ('A3', 'I3'): 3.5})

    def test_tableU(self):
        # Importing a 2D array of parameters.
        self.check_skiplist('tableU')
        dp = DataPortal()
        dp.load(format='array', param='U', **self.create_options('U'))
        self.assertEqual(dp.data('U'), {('I2', 'A1'): 1.4, ('I3', 'A1'): 1.5, ('I3', 'A2'): 2.5, ('I4', 'A1'): 1.6, ('I3', 'A3'): 3.5, ('I1', 'A2'): 2.3, ('I4', 'A3'): 3.6, ('I1', 'A3'): 3.3, ('I4', 'A2'): 2.6, ('I2', 'A3'): 3.4, ('I1', 'A1'): 1.3, ('I2', 'A2'): 2.4})

    def test_tableS(self):
        # Importing a table, but only reporting the values for the non-index
        # parameter columns.  The first column is assumed to represent an
        # index column.  A missing value is represented in the column data.
        self.check_skiplist('tableS')
        dp = DataPortal()
        dp.load(param='S', **self.create_options('S'))
        self.assertEqual(dp.data('S'), {'A1':3.3,'A3':3.5})

    def test_tablePO(self):
        # Importing a table that has multiple indexing columns
        self.check_skiplist('tablePO')
        dp = DataPortal()
        dp.load(index='J', param=('P', 'O'), **self.create_options('PO'))
        self.assertEqual(set(dp.data('J')), set([('A3', 'B3'), ('A1', 'B1'), ('A2', 'B2')]) )
        self.assertEqual(dp.data('P'), {('A3', 'B3'): 4.5, ('A1', 'B1'): 4.3, ('A2', 'B2'): 4.4} )
        self.assertEqual(dp.data('O'), {('A3', 'B3'): 5.5, ('A1', 'B1'): 5.3, ('A2', 'B2'): 5.4})


class TestOnlyCsvPortal(TestOnlyTextPortal):

    suffix = '.csv'

    def create_options(self, name):
        return {'filename':os.path.abspath(tutorial_dir+os.sep+'csv'+os.sep+name+self.suffix)}


class TestOnlyXmlPortal(TestOnlyTextPortal):

    suffix = '.xml'
    skiplist = ['tableD', 'tableT', 'tableU']

    def create_options(self, name):
        return {'filename':os.path.abspath(tutorial_dir+os.sep+'xml'+os.sep+name+self.suffix)}


class TestOnlyJsonPortal(TestOnlyTextPortal):

    suffix = '.json'
    skiplist = ['tableD', 'tableT', 'tableU', 'tableXW_4']

    def create_options(self, name):
        return {'filename':os.path.abspath(tutorial_dir+os.sep+'json'+os.sep+name+self.suffix)}

    def test_store_set1(self):
        # Write 1-D set
        self.check_skiplist('store_set1')
        model = ConcreteModel()
        model.A = Set(initialize=set([1,3,5]))
        data = DataPortal()
        data.store(set=model.A, **self.create_write_options('set1'))
        if self.suffix == '.json':
            self.assertMatchesJsonBaseline(currdir+'set1'+self.suffix, currdir+'set1.baseline'+self.suffix)
        else:
            self.assertFileEqualsBaseline(currdir+'set1'+self.suffix, currdir+'set1.baseline'+self.suffix)

    def test_store_set1(self):
        # Write 1-D set
        model = ConcreteModel()
        model.A = Set(initialize=set([1,3,5]))
        data = DataPortal()
        data.store(data=model.A, **self.create_write_options('set1'))
        if self.suffix == '.json':
            self.assertMatchesJsonBaseline(currdir+'set1'+self.suffix, currdir+'set1.baseline'+self.suffix)
        else:
            self.assertFileEqualsBaseline(currdir+'set1'+self.suffix, currdir+'set1.baseline'+self.suffix)

    def test_store_set2(self):
        # Write 2-D set
        model = ConcreteModel()
        model.A = Set(initialize=set([(1,2),(3,4),(5,6)]), dimen=2)
        data = DataPortal()
        data.store(data=model.A, **self.create_write_options('set2'))
        if self.suffix == '.json':
            self.assertMatchesJsonBaseline(currdir+'set2'+self.suffix, currdir+'set2.baseline'+self.suffix)
        else:
            self.assertFileEqualsBaseline(currdir+'set2'+self.suffix, currdir+'set2.baseline'+self.suffix)

    def test_store_param1(self):
        # Write scalar param
        model = ConcreteModel()
        model.p = Param(initialize=1)
        data = DataPortal()
        data.store(data=model.p, **self.create_write_options('param1'))
        if self.suffix == '.json':
            self.assertMatchesJsonBaseline(currdir+'param1'+self.suffix, currdir+'param1.baseline'+self.suffix)
        else:
            self.assertFileEqualsBaseline(currdir+'param1'+self.suffix, currdir+'param1.baseline'+self.suffix)

    def test_store_param2(self):
        # Write 1-D param
        model = ConcreteModel()
        model.A = Set(initialize=set([1,2,3]))
        model.p = Param(model.A, initialize={1:10, 2:20, 3:30})
        data = DataPortal()
        data.store(data=model.p, **self.create_write_options('param2'))
        if self.suffix == '.json':
            self.assertMatchesJsonBaseline(currdir+'param2'+self.suffix, currdir+'param2.baseline'+self.suffix)
        else:
            self.assertFileEqualsBaseline(currdir+'param2'+self.suffix, currdir+'param2.baseline'+self.suffix)

    def test_store_param3(self):
        # Write 2-D params
        model = ConcreteModel()
        model.A = Set(initialize=set([(1,2),(2,3),(3,4)]), dimen=2)
        model.p = Param(model.A, initialize={(1,2):10, (2,3):20, (3,4):30})
        model.q = Param(model.A, initialize={(1,2):11, (2,3):21, (3,4):31})
        data = DataPortal()
        data.store(data=(model.p,model.q), **self.create_write_options('param3'))
        if self.suffix == '.json':
            self.assertMatchesJsonBaseline(currdir+'param3'+self.suffix, currdir+'param3.baseline'+self.suffix)
        else:
            self.assertFileEqualsBaseline(currdir+'param3'+self.suffix, currdir+'param3.baseline'+self.suffix)

    def test_store_param4(self):
        # Write 2-D params
        model = ConcreteModel()
        model.A = Set(initialize=set([(1,2),(2,3),(3,4)]), dimen=2)
        model.p = Param(model.A, initialize={(1,2):10, (2,3):20, (3,4):30})
        model.q = Param(model.A, initialize={(1,2):11, (2,3):21, (3,4):31})
        data = DataPortal()
        data.store(data=(model.p,model.q), columns=('a','b','c','d'), **self.create_write_options('param4'))
        if self.suffix == '.json':
            self.assertMatchesJsonBaseline(currdir+'param4'+self.suffix, currdir+'param4.baseline'+self.suffix)
        else:
            self.assertFileEqualsBaseline(currdir+'param4'+self.suffix, currdir+'param4.baseline'+self.suffix)


@unittest.skipIf(not yaml_interface, "No YAML interface available")
class TestOnlyYamlPortal(TestOnlyJsonPortal):

    suffix = '.yaml'

    def create_options(self, name):
        return {'filename':os.path.abspath(tutorial_dir+os.sep+'yaml'+os.sep+name+self.suffix)}

class TestTextPortal(unittest.TestCase):

    suffix = '.tab'
    skiplist = []

    def check_skiplist(self, name):
        if name in self.skiplist:
            self.skipTest('Skipping test %s' % name)

    def create_options(self, name):
        return {'filename':os.path.abspath(tutorial_dir+os.sep+'tab'+os.sep+name+self.suffix)}

    def create_write_options(self, name):
        return {'filename':os.path.abspath(currdir+os.sep+name+self.suffix)}

    def test_tableA(self):
        # Importing an unordered set of arbitrary data
        self.check_skiplist('tableA')
        model=AbstractModel()
        model.A = Set()
        data = DataPortal()
        data.load(set=model.A, **self.create_options('A'))
        instance = model.create(data)
        self.assertEqual(instance.A.data(), set(['A1', 'A2', 'A3']))

    def test_tableB(self):
        # Importing an unordered set of numeric data
        self.check_skiplist('tableB')
        model=AbstractModel()
        model.B = Set()
        data = DataPortal()
        data.load(set=model.B, **self.create_options('B'))
        instance = model.create(data)
        self.assertEqual(instance.B.data(), set([1, 2, 3]))

    def test_tableC(self):
        # Importing a multi-column table, where all columns are
        #treated as values for a set with tuple values.
        self.check_skiplist('tableC')
        model=AbstractModel()
        model.C = Set(dimen=2)
        data = DataPortal()
        data.load(set=model.C, **self.create_options('C'))
        instance = model.create(data)
        self.assertEqual(instance.C.data(), set([('A1',1), ('A1',2), ('A1',3), ('A2',1), ('A2',2), ('A2',3), ('A3',1), ('A3',2), ('A3',3)]))

    def test_tableD(self):
        # Importing a 2D array of data as a set.
        self.check_skiplist('tableD')
        model=AbstractModel()
        model.C = Set(dimen=2)
        data = DataPortal()
        data.load(set=model.C, format='set_array', **self.create_options('D'))
        instance = model.create(data)
        self.assertEqual(instance.C.data(), set([('A1',1), ('A2',2), ('A3',3)]))

    def test_tableZ(self):
        # Importing a single parameter
        self.check_skiplist('tableZ')
        model=AbstractModel()
        model.Z = Param(default=99.0)
        data = DataPortal()
        data.load(param=model.Z, **self.create_options('Z'))
        instance = model.create(data)
        self.assertEqual(instance.Z, 1.1)

    def test_tableY(self):
        # Same as tableXW.
        self.check_skiplist('tableY')
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.Y = Param(model.A)
        data = DataPortal()
        data.load(param=model.Y, **self.create_options('Y'))
        instance = model.create(data)
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.Y.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})

    def test_tableXW_1(self):
        # Importing a table, but only reporting the values for the non-index
        #parameter columns.  The first column is assumed to represent an
        #index column.
        self.check_skiplist('tableXW_1')
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.X = Param(model.A)
        model.W = Param(model.A)
        data = DataPortal()
        data.load(param=(model.X, model.W), **self.create_options('XW'))
        instance = model.create(data)
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.X.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.W.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})

    def test_tableXW_2(self):
        # Like test_tableXW_1, except that set A is not defined.
        self.check_skiplist('tableXW_2')
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3'])
        model.X = Param(model.A)
        model.W = Param(model.A)
        data = DataPortal()
        data.load(param=(model.X, model.W), **self.create_options('XW'))
        instance = model.create(data)
        self.assertEqual(instance.A.data(), set(['A1','A2','A3']))
        self.assertEqual(instance.X.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.W.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})

    def test_tableXW_3(self):
        # Like test_tableXW_1, except that set A is defined in the import statment.
        self.check_skiplist('tableXW_3')
        model=AbstractModel()
        model.A = Set()
        model.X = Param(model.A)
        model.W = Param(model.A)
        data = DataPortal()
        data.load(index=model.A, param=(model.X, model.W), **self.create_options('XW'))
        instance = model.create(data)
        self.assertEqual(instance.A.data(), set(['A1','A2','A3']))
        self.assertEqual(instance.X.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.W.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})

    def test_tableXW_4(self):
        # Like test_tableXW_1, except that set A is defined in the import statment and all values are mapped.
        self.check_skiplist('tableXW_4')
        model=AbstractModel()
        model.B = Set()
        model.R = Param(model.B)
        model.S = Param(model.B)
        data = DataPortal()
        data.load(select=('A', 'W', 'X'), index=model.B, param=(model.R, model.S), **self.create_options('XW'))
        instance = model.create(data)
        self.assertEqual(instance.B.data(), set(['A1','A2','A3']))
        self.assertEqual(instance.S.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.R.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})

    def test_tableT(self):
        # Importing a 2D array of parameters that are transposed.
        self.check_skiplist('tableT')
        model=AbstractModel()
        model.B = Set(initialize=['I1','I2','I3','I4'])
        model.A = Set(initialize=['A1','A2','A3'])
        model.T = Param(model.A, model.B)
        data = DataPortal()
        data.load(format='transposed_array', param=model.T, **self.create_options('T'))
        instance = model.create(data)
        self.assertEqual(instance.T.extract_values(), {('A2', 'I1'): 2.3, ('A1', 'I2'): 1.4, ('A1', 'I3'): 1.5, ('A1', 'I4'): 1.6, ('A1', 'I1'): 1.3, ('A3', 'I4'): 3.6, ('A2', 'I4'): 2.6, ('A3', 'I1'): 3.3, ('A2', 'I3'): 2.5, ('A3', 'I2'): 3.4, ('A2', 'I2'): 2.4, ('A3', 'I3'): 3.5})

    def test_tableU(self):
        # Importing a 2D array of parameters.
        self.check_skiplist('tableU')
        model=AbstractModel()
        model.A = Set(initialize=['I1','I2','I3','I4'])
        model.B = Set(initialize=['A1','A2','A3'])
        model.U = Param(model.A, model.B)
        data = DataPortal()
        data.load(format='array', param=model.U, **self.create_options('U'))
        instance = model.create(data)
        self.assertEqual(instance.U.extract_values(), {('I2', 'A1'): 1.4, ('I3', 'A1'): 1.5, ('I3', 'A2'): 2.5, ('I4', 'A1'): 1.6, ('I3', 'A3'): 3.5, ('I1', 'A2'): 2.3, ('I4', 'A3'): 3.6, ('I1', 'A3'): 3.3, ('I4', 'A2'): 2.6, ('I2', 'A3'): 3.4, ('I1', 'A1'): 1.3, ('I2', 'A2'): 2.4})

    def test_tableS(self):
        # Importing a table, but only reporting the values for the non-index
        #parameter columns.  The first column is assumed to represent an
        #index column.  A missing value is represented in the column data.
        self.check_skiplist('tableS')
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.S = Param(model.A)
        data = DataPortal()
        data.load(param=model.S, **self.create_options('S'))
        instance = model.create(data)
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.S.extract_values(), {'A1':3.3,'A3':3.5})

    def test_tablePO(self):
        # Importing a table that has multiple indexing columns
        self.check_skiplist('tablePO')
        model=AbstractModel()
        model.J = Set(dimen=2)
        model.P = Param(model.J)
        model.O = Param(model.J)
        data = DataPortal()
        data.load(index=model.J, param=(model.P, model.O), **self.create_options('PO'))
        instance = model.create(data)
        self.assertEqual(instance.J.data(), set([('A3', 'B3'), ('A1', 'B1'), ('A2', 'B2')]) )
        self.assertEqual(instance.P.extract_values(), {('A3', 'B3'): 4.5, ('A1', 'B1'): 4.3, ('A2', 'B2'): 4.4} )
        self.assertEqual(instance.O.extract_values(), {('A3', 'B3'): 5.5, ('A1', 'B1'): 5.3, ('A2', 'B2'): 5.4})

    def test_store_set1(self):
        # Write 1-D set
        self.check_skiplist('store_set1')
        model = ConcreteModel()
        model.A = Set(initialize=set([1,3,5]))
        data = DataPortal()
        data.store(set=model.A, **self.create_write_options('set1'))
        self.assertFileEqualsBaseline(currdir+'set1'+self.suffix, currdir+'set1.baseline'+self.suffix)

    def test_store_set2(self):
        # Write 2-D set
        self.check_skiplist('store_set2')
        model = ConcreteModel()
        model.A = Set(initialize=set([(1,2),(3,4),(5,6)]), dimen=2)
        data = DataPortal()
        data.store(set=model.A, **self.create_write_options('set2'))
        self.assertFileEqualsBaseline(currdir+'set2'+self.suffix, currdir+'set2.baseline'+self.suffix)

    def test_store_param1(self):
        # Write scalar param
        self.check_skiplist('store_param1')
        model = ConcreteModel()
        model.p = Param(initialize=1)
        data = DataPortal()
        data.store(param=model.p, **self.create_write_options('param1'))
        self.assertFileEqualsBaseline(currdir+'param1'+self.suffix, currdir+'param1.baseline'+self.suffix)

    def test_store_param2(self):
        # Write 1-D param
        self.check_skiplist('store_param2')
        model = ConcreteModel()
        model.A = Set(initialize=set([1,2,3]))
        model.p = Param(model.A, initialize={1:10, 2:20, 3:30})
        data = DataPortal()
        data.store(param=model.p, **self.create_write_options('param2'))
        self.assertFileEqualsBaseline(currdir+'param2'+self.suffix, currdir+'param2.baseline'+self.suffix)

    def test_store_param3(self):
        # Write 2-D params
        self.check_skiplist('store_param3')
        model = ConcreteModel()
        model.A = Set(initialize=set([(1,2),(2,3),(3,4)]), dimen=2)
        model.p = Param(model.A, initialize={(1,2):10, (2,3):20, (3,4):30})
        model.q = Param(model.A, initialize={(1,2):11, (2,3):21, (3,4):31})
        data = DataPortal()
        data.store(param=(model.p,model.q), **self.create_write_options('param3'))
        if self.suffix == '.json':
            self.assertMatchesJsonBaseline(currdir+'param3'+self.suffix, currdir+'param3.baseline'+self.suffix)
        else:
            self.assertFileEqualsBaseline(currdir+'param3'+self.suffix, currdir+'param3.baseline'+self.suffix)

    def test_store_param4(self):
        # Write 2-D params
        self.check_skiplist('store_param4')
        model = ConcreteModel()
        model.A = Set(initialize=set([(1,2),(2,3),(3,4)]), dimen=2)
        model.p = Param(model.A, initialize={(1,2):10, (2,3):20, (3,4):30})
        model.q = Param(model.A, initialize={(1,2):11, (2,3):21, (3,4):31})
        data = DataPortal()
        data.store(param=(model.p,model.q), columns=('a','b','c','d'), **self.create_write_options('param4'))
        if self.suffix == '.json':
            self.assertMatchesJsonBaseline(currdir+'param4'+self.suffix, currdir+'param4.baseline'+self.suffix)
        else:
            self.assertFileEqualsBaseline(currdir+'param4'+self.suffix, currdir+'param4.baseline'+self.suffix)


class TestCsvPortal(TestTextPortal):

    suffix = '.csv'

    def create_options(self, name):
        return {'filename':os.path.abspath(tutorial_dir+os.sep+'csv'+os.sep+name+self.suffix)}


class TestXmlPortal(TestTextPortal):

    suffix = '.xml'
    skiplist = ['tableD', 'tableT', 'tableU']

    def create_options(self, name):
        return {'filename':os.path.abspath(tutorial_dir+os.sep+'xml'+os.sep+name+self.suffix)}


class TestJsonPortal(TestTextPortal):

    suffix = '.json'
    skiplist = ['tableD', 'tableT', 'tableU', 'tableXW_4']

    def create_options(self, name):
        return {'filename':os.path.abspath(tutorial_dir+os.sep+'json'+os.sep+name+self.suffix)}


@unittest.skipIf(not yaml_available, "YAML not available available")
class TestYamlPortal(TestTextPortal):

    suffix = '.yaml'
    skiplist = ['tableD', 'tableT', 'tableU', 'tableXW_4']

    def create_options(self, name):
        return {'filename':os.path.abspath(tutorial_dir+os.sep+'yaml'+os.sep+name+self.suffix)}


class ImportTests(object):

    skiplist = []

    def check_skiplist(self, name):
        if name in self.skiplist:
            self.skipTest('Skipping test %s' % name)

    def filename(self, tname):
        return os.path.abspath(tutorial_dir+os.sep+self.suffix+os.sep+tname+'.'+self.suffix)

    def test_tableA1(self):
        # Importing a single column of data
        self.check_skiplist('tableA1')
        pyutilib.misc.setup_redirect(currdir+'importA1.dat')
        print("import "+self.filename('A')+" format=set: A;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set()
        instance = model.create(currdir+'importA1.dat')
        self.assertEqual(instance.A.data(), set(['A1', 'A2', 'A3']))
        os.remove(currdir+'importA1.dat')

    def test_tableA2(self):
        # Importing a single column of data
        self.check_skiplist('tableA2')
        pyutilib.misc.setup_redirect(currdir+'importA2.dat')
        print("import "+self.filename('A')+" ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set()
        try:
            instance = model.create(currdir+'importA2.dat')
            self.fail("Should fail because no set name is specified")
        except IOError:
            pass
        os.remove(currdir+'importA2.dat')

    def test_tableA3(self):
        # Importing a single column of data
        self.check_skiplist('tableA3')
        pyutilib.misc.setup_redirect(currdir+'importA3.dat')
        print("import "+self.filename('A')+" : A ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set()
        instance = model.create(currdir+'importA3.dat')
        self.assertEqual(instance.A.data(), set(['A1', 'A2', 'A3']))
        os.remove(currdir+'importA3.dat')

    def test_tableB1(self):
        # Same as test_tableA
        self.check_skiplist('tableB1')
        pyutilib.misc.setup_redirect(currdir+'importB.dat')
        print("import "+self.filename('B')+" :B;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.B = Set()
        instance = model.create(currdir+'importB.dat')
        self.assertEqual(instance.B.data(), set([1, 2, 3]))
        os.remove(currdir+'importB.dat')

    def test_tableC(self):
        # Importing a multi-column table, where all columns are
        # treated as values for a set with tuple values.
        self.check_skiplist('tableC')
        pyutilib.misc.setup_redirect(currdir+'importC.dat')
        print("import "+self.filename('C')+" : C ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.C = Set(dimen=2)
        instance = model.create(currdir+'importC.dat')
        self.assertEqual(instance.C.data(), set([('A1',1), ('A1',2), ('A1',3), ('A2',1), ('A2',2), ('A2',3), ('A3',1), ('A3',2), ('A3',3)]))
        os.remove(currdir+'importC.dat')

    def test_tableD(self):
        # Importing a 2D array of data as a set.
        self.check_skiplist('tableD')
        pyutilib.misc.setup_redirect(currdir+'importD.dat')
        print("import "+self.filename('D')+" format=set_array: C ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.C = Set(dimen=2)
        instance = model.create(currdir+'importD.dat')
        self.assertEqual(instance.C.data(), set([('A1',1), ('A2',2), ('A3',3)]))
        os.remove(currdir+'importD.dat')

    def test_tableZ(self):
        # Importing a single parameter
        self.check_skiplist('tableZ')
        pyutilib.misc.setup_redirect(currdir+'importZ.dat')
        print("import "+self.filename('Z')+" : Z ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.Z = Param(default=99.0)
        instance = model.create(currdir+'importZ.dat')
        self.assertEqual(instance.Z, 1.1)
        os.remove(currdir+'importZ.dat')

    def test_tableY(self):
        # Same as tableXW.
        self.check_skiplist('tableY')
        pyutilib.misc.setup_redirect(currdir+'importY.dat')
        print("import "+self.filename('Y')+" : [A] Y;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.Y = Param(model.A)
        instance = model.create(currdir+'importY.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.Y.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        os.remove(currdir+'importY.dat')

    def test_tableXW_1(self):
        # Importing a table, but only reporting the values for the non-index
        # parameter columns.  The first column is assumed to represent an
        # index column.
        self.check_skiplist('tableXW_1')
        pyutilib.misc.setup_redirect(currdir+'importXW.dat')
        print("import "+self.filename('XW')+": [A] X W;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.X = Param(model.A)
        model.W = Param(model.A)
        instance = model.create(currdir+'importXW.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.X.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.W.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})
        os.remove(currdir+'importXW.dat')

    def test_tableXW_2(self):
        # Like test_tableXW_1, except that set A is not defined.
        self.check_skiplist('tableXW_2')
        pyutilib.misc.setup_redirect(currdir+'importXW.dat')
        print("import "+self.filename('XW')+": [A] X W;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3'])
        model.X = Param(model.A)
        model.W = Param(model.A)
        instance = model.create(currdir+'importXW.dat')
        self.assertEqual(instance.X.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.W.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})
        os.remove(currdir+'importXW.dat')

    def test_tableXW_3(self):
        # Like test_tableXW_1, except that set A is defined in the import statment.
        self.check_skiplist('tableXW_3')
        pyutilib.misc.setup_redirect(currdir+'importXW.dat')
        print("import "+self.filename('XW')+": A=[A] X W;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set()
        model.X = Param(model.A)
        model.W = Param(model.A)
        instance = model.create(currdir+'importXW.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3']))
        self.assertEqual(instance.X.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.W.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})
        os.remove(currdir+'importXW.dat')

    def test_tableXW_4(self):
        # Like test_tableXW_1, except that set A is defined in the import statment and all values are mapped.
        self.check_skiplist('tableXW_4')
        pyutilib.misc.setup_redirect(currdir+'importXW.dat')
        print("import "+self.filename('XW')+": B=[A] R=X S=W;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.B = Set()
        model.R = Param(model.B)
        model.S = Param(model.B)
        instance = model.create(currdir+'importXW.dat')
        self.assertEqual(instance.B.data(), set(['A1','A2','A3']))
        self.assertEqual(instance.R.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.S.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})
        os.remove(currdir+'importXW.dat')

    def test_tableT(self):
        # Importing a 2D array of parameters that are transposed.
        self.check_skiplist('tableT')
        pyutilib.misc.setup_redirect(currdir+'importT.dat')
        print("import "+self.filename('T')+" format=transposed_array : T;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.B = Set(initialize=['I1','I2','I3','I4'])
        model.A = Set(initialize=['A1','A2','A3'])
        model.T = Param(model.A, model.B)
        instance = model.create(currdir+'importT.dat')
        self.assertEqual(instance.T.extract_values(), {('A2', 'I1'): 2.3, ('A1', 'I2'): 1.4, ('A1', 'I3'): 1.5, ('A1', 'I4'): 1.6, ('A1', 'I1'): 1.3, ('A3', 'I4'): 3.6, ('A2', 'I4'): 2.6, ('A3', 'I1'): 3.3, ('A2', 'I3'): 2.5, ('A3', 'I2'): 3.4, ('A2', 'I2'): 2.4, ('A3', 'I3'): 3.5})
        os.remove(currdir+'importT.dat')

    def test_tableU(self):
        # Importing a 2D array of parameters.
        self.check_skiplist('tableU')
        pyutilib.misc.setup_redirect(currdir+'importU.dat')
        print("import "+self.filename('U')+" format=array : U;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['I1','I2','I3','I4'])
        model.B = Set(initialize=['A1','A2','A3'])
        model.U = Param(model.A, model.B)
        instance = model.create(currdir+'importU.dat')
        self.assertEqual(instance.U.extract_values(), {('I2', 'A1'): 1.4, ('I3', 'A1'): 1.5, ('I3', 'A2'): 2.5, ('I4', 'A1'): 1.6, ('I3', 'A3'): 3.5, ('I1', 'A2'): 2.3, ('I4', 'A3'): 3.6, ('I1', 'A3'): 3.3, ('I4', 'A2'): 2.6, ('I2', 'A3'): 3.4, ('I1', 'A1'): 1.3, ('I2', 'A2'): 2.4})
        os.remove(currdir+'importU.dat')

    def test_tableS(self):
        # Importing a table, but only reporting the values for the non-index
        # parameter columns.  The first column is assumed to represent an
        # index column.  A missing value is represented in the column data.
        self.check_skiplist('tableS')
        pyutilib.misc.setup_redirect(currdir+'importS.dat')
        print("import "+self.filename('S')+": [A] S ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.S = Param(model.A)
        instance = model.create(currdir+'importS.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.S.extract_values(), {'A1':3.3,'A3':3.5})
        os.remove(currdir+'importS.dat')

    def test_tablePO(self):
        # Importing a table that has multiple indexing columns
        self.check_skiplist('tablePO')
        pyutilib.misc.setup_redirect(currdir+'importPO.dat')
        print("import "+self.filename('PO')+" : J=[A,B] P O;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.J = Set(dimen=2)
        model.P = Param(model.J)
        model.O = Param(model.J)
        instance = model.create(currdir+'importPO.dat')
        self.assertEqual(instance.J.data(), set([('A3', 'B3'), ('A1', 'B1'), ('A2', 'B2')]) )
        self.assertEqual(instance.P.extract_values(), {('A3', 'B3'): 4.5, ('A1', 'B1'): 4.3, ('A2', 'B2'): 4.4} )
        self.assertEqual(instance.O.extract_values(), {('A3', 'B3'): 5.5, ('A1', 'B1'): 5.3, ('A2', 'B2'): 5.4})
        os.remove(currdir+'importPO.dat')


class TestTextImport(ImportTests, unittest.TestCase):

    suffix = 'tab'


class TestCsvImport(ImportTests, unittest.TestCase):

    suffix = 'csv'


class TestXmlImport(ImportTests, unittest.TestCase):

    suffix = 'xml'
    skiplist = ['tableD', 'tableT', 'tableU']

    def test_tableXW_nested1(self):
        # Importing a table, but only reporting the values for the non-index
        # parameter columns.  The first column is assumed to represent an
        # index column.
        self.check_skiplist('tableXW_1')
        pyutilib.misc.setup_redirect(currdir+'importXW.dat')
        print("import "+self.filename('XW_nested1')+" query='./bar/table/*' : [A] X W;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.X = Param(model.A)
        model.W = Param(model.A)
        instance = model.create(currdir+'importXW.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.X.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.W.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})
        os.remove(currdir+'importXW.dat')

    def test_tableXW_nested2(self):
        # Importing a table, but only reporting the values for the non-index
        # parameter columns.  The first column is assumed to represent an
        # index column.
        self.check_skiplist('tableXW_1')
        pyutilib.misc.setup_redirect(currdir+'importXW.dat')
        print("import "+self.filename('XW_nested2')+" query='./bar/table/row' : [A] X W;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.X = Param(model.A)
        model.W = Param(model.A)
        instance = model.create(currdir+'importXW.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.X.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.W.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})
        os.remove(currdir+'importXW.dat')


class SpreadsheetImport(ImportTests):

    def filename(self, tname):
        return os.path.abspath(tutorial_dir+os.sep+self._filename)+" range="+tname+"table"


@unittest.skipIf(not xls_interface, "No XLS interface available")
class TestSpreadsheetXLSImport(SpreadsheetImport, unittest.TestCase):

    _filename='excel.xls'


@unittest.skipIf(not xlsx_interface, "No XLSX interface available")
class TestSpreadsheetXLSXImport(SpreadsheetImport, unittest.TestCase):

    _filename='excel.xlsx'


@unittest.skipIf(not xlsb_interface, "No XLSB interface available")
class TestSpreadsheetXLSBImport(SpreadsheetImport, unittest.TestCase):

    _filename='excel.xlsb'


@unittest.skipIf(not xlsm_interface, "No XLSM interface available")
class TestSpreadsheetXLSMImport(SpreadsheetImport, unittest.TestCase):

    _filename='excel.xlsm'



class LoadTests(object):

    skiplist = []

    def check_skiplist(self, name):
        self.skipTest('Skipping load tests')

    def Xcheck_skiplist(self, name):
        if name in self.skiplist:
            self.skipTest('Skipping test %s' % name)

    def filename(self, tname):
        return os.path.abspath(tutorial_dir+os.sep+self.suffix+os.sep+tname+'.'+self.suffix)

    def test_tableA1(self):
        # Importing a single column of data
        self.check_skiplist('tableA1')
        pyutilib.misc.setup_redirect(currdir+'importA1.dat')
        print("load "+self.filename('A')+" A={A};")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set()
        instance = model.create(currdir+'importA1.dat')
        self.assertEqual(instance.A.data(), set(['A1', 'A2', 'A3']))
        os.remove(currdir+'importA1.dat')

    def test_tableA2(self):
        # Importing a single column of data
        self.check_skiplist('tableA2')
        pyutilib.misc.setup_redirect(currdir+'importA2.dat')
        print("load "+self.filename('A')+" ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set()
        try:
            instance = model.create(currdir+'importA2.dat')
            self.fail("Should fail because no set name is specified")
        except IOError:
            pass
        os.remove(currdir+'importA2.dat')

    def test_tableA3(self):
        # Importing a single column of data
        self.check_skiplist('tableA3')
        pyutilib.misc.setup_redirect(currdir+'importA3.dat')
        print("load "+self.filename('A')+" A={A} ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set()
        instance = model.create(currdir+'importA3.dat')
        self.assertEqual(instance.A.data(), set(['A1', 'A2', 'A3']))
        os.remove(currdir+'importA3.dat')

    def test_tableB1(self):
        # Same as test_tableA
        self.check_skiplist('tableB1')
        pyutilib.misc.setup_redirect(currdir+'importB.dat')
        print("load "+self.filename('B')+" B={B};")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.B = Set()
        instance = model.create(currdir+'importB.dat')
        self.assertEqual(instance.B.data(), set([1, 2, 3]))
        os.remove(currdir+'importB.dat')

    def test_tableC(self):
        # Importing a multi-column table, where all columns are
        # treated as values for a set with tuple values.
        self.check_skiplist('tableC')
        pyutilib.misc.setup_redirect(currdir+'importC.dat')
        print("load "+self.filename('C')+" C={A,B} ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.C = Set(dimen=2)
        instance = model.create(currdir+'importC.dat')
        self.assertEqual(instance.C.data(), set([('A1',1), ('A1',2), ('A1',3), ('A2',1), ('A2',2), ('A2',3), ('A3',1), ('A3',2), ('A3',3)]))
        os.remove(currdir+'importC.dat')

    def test_tableD(self):
        # Importing a 2D array of data as a set.
        self.check_skiplist('tableD')
        pyutilib.misc.setup_redirect(currdir+'importD.dat')
        print("load "+self.filename('D')+" format=set_array: C ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.C = Set(dimen=2)
        instance = model.create(currdir+'importD.dat')
        self.assertEqual(instance.C.data(), set([('A1',1), ('A2',2), ('A3',3)]))
        os.remove(currdir+'importD.dat')

    def test_tableZ(self):
        # Importing a single parameter
        self.check_skiplist('tableZ')
        pyutilib.misc.setup_redirect(currdir+'importZ.dat')
        print("load "+self.filename('Z')+" Z ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.Z = Param(default=99.0)
        instance = model.create(currdir+'importZ.dat')
        self.assertEqual(instance.Z, 1.1)
        os.remove(currdir+'importZ.dat')

    def test_tableY(self):
        # Same as tableXW.
        self.check_skiplist('tableY')
        pyutilib.misc.setup_redirect(currdir+'importY.dat')
        print("load "+self.filename('Y')+" Y(A);")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.Y = Param(model.A)
        instance = model.create(currdir+'importY.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.Y.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        os.remove(currdir+'importY.dat')

    def test_tableXW_1(self):
        # Importing a table, but only reporting the values for the non-index
        # parameter columns.  The first column is assumed to represent an
        # index column.
        self.check_skiplist('tableXW_1')
        pyutilib.misc.setup_redirect(currdir+'importXW.dat')
        print("load "+self.filename('XW')+" X(A) W(A);")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.X = Param(model.A)
        model.W = Param(model.A)
        instance = model.create(currdir+'importXW.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.X.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.W.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})
        os.remove(currdir+'importXW.dat')

    def test_tableXW_2(self):
        # Like test_tableXW_1, except that set A is not defined.
        self.check_skiplist('tableXW_2')
        pyutilib.misc.setup_redirect(currdir+'importXW.dat')
        print("load "+self.filename('XW')+" X(A) W(A);")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3'])
        model.X = Param(model.A)
        model.W = Param(model.A)
        instance = model.create(currdir+'importXW.dat')
        self.assertEqual(instance.X.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.W.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})
        os.remove(currdir+'importXW.dat')

    def test_tableXW_3(self):
        # Like test_tableXW_1, except that set A is defined in the load statment.
        self.check_skiplist('tableXW_3')
        pyutilib.misc.setup_redirect(currdir+'importXW.dat')
        print("load "+self.filename('XW')+" A={A} X(A) W(A);")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set()
        model.X = Param(model.A)
        model.W = Param(model.A)
        instance = model.create(currdir+'importXW.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3']))
        self.assertEqual(instance.X.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.W.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})
        os.remove(currdir+'importXW.dat')

    def test_tableXW_4(self):
        # Like test_tableXW_1, except that set A is defined in the load statment and all values are mapped.
        self.check_skiplist('tableXW_4')
        pyutilib.misc.setup_redirect(currdir+'importXW.dat')
        print("load "+self.filename('XW')+" B={A} R(A)={X} S(A)={W};")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.B = Set()
        model.R = Param(model.B)
        model.S = Param(model.B)
        instance = model.create(currdir+'importXW.dat')
        self.assertEqual(instance.B.data(), set(['A1','A2','A3']))
        self.assertEqual(instance.R.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.S.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})
        os.remove(currdir+'importXW.dat')

    def test_tableT(self):
        # Importing a 2D array of parameters that are transposed.
        self.check_skiplist('tableT')
        pyutilib.misc.setup_redirect(currdir+'importT.dat')
        print("load "+self.filename('T')+" format=transposed_array T;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.B = Set(initialize=['I1','I2','I3','I4'])
        model.A = Set(initialize=['A1','A2','A3'])
        model.T = Param(model.A, model.B)
        instance = model.create(currdir+'importT.dat')
        self.assertEqual(instance.T.extract_values(), {('A2', 'I1'): 2.3, ('A1', 'I2'): 1.4, ('A1', 'I3'): 1.5, ('A1', 'I4'): 1.6, ('A1', 'I1'): 1.3, ('A3', 'I4'): 3.6, ('A2', 'I4'): 2.6, ('A3', 'I1'): 3.3, ('A2', 'I3'): 2.5, ('A3', 'I2'): 3.4, ('A2', 'I2'): 2.4, ('A3', 'I3'): 3.5})
        os.remove(currdir+'importT.dat')

    def test_tableU(self):
        # Importing a 2D array of parameters.
        self.check_skiplist('tableU')
        pyutilib.misc.setup_redirect(currdir+'importU.dat')
        print("load "+self.filename('U')+" format=array U;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['I1','I2','I3','I4'])
        model.B = Set(initialize=['A1','A2','A3'])
        model.U = Param(model.A, model.B)
        instance = model.create(currdir+'importU.dat')
        self.assertEqual(instance.U.extract_values(), {('I2', 'A1'): 1.4, ('I3', 'A1'): 1.5, ('I3', 'A2'): 2.5, ('I4', 'A1'): 1.6, ('I3', 'A3'): 3.5, ('I1', 'A2'): 2.3, ('I4', 'A3'): 3.6, ('I1', 'A3'): 3.3, ('I4', 'A2'): 2.6, ('I2', 'A3'): 3.4, ('I1', 'A1'): 1.3, ('I2', 'A2'): 2.4})
        os.remove(currdir+'importU.dat')

    def test_tableS(self):
        # Importing a table, but only reporting the values for the non-index
        # parameter columns.  The first column is assumed to represent an
        # index column.  A missing value is represented in the column data.
        self.check_skiplist('tableS')
        pyutilib.misc.setup_redirect(currdir+'importS.dat')
        print("load "+self.filename('S')+" S(A) ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.S = Param(model.A)
        instance = model.create(currdir+'importS.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.S.extract_values(), {'A1':3.3,'A3':3.5})
        os.remove(currdir+'importS.dat')

    def test_tablePO(self):
        # Importing a table that has multiple indexing columns
        self.check_skiplist('tablePO')
        pyutilib.misc.setup_redirect(currdir+'importPO.dat')
        print("load "+self.filename('PO')+" J={A,B} P(J) O(J);")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.J = Set(dimen=2)
        model.P = Param(model.J)
        model.O = Param(model.J)
        instance = model.create(currdir+'importPO.dat')
        self.assertEqual(instance.J.data(), set([('A3', 'B3'), ('A1', 'B1'), ('A2', 'B2')]) )
        self.assertEqual(instance.P.extract_values(), {('A3', 'B3'): 4.5, ('A1', 'B1'): 4.3, ('A2', 'B2'): 4.4} )
        self.assertEqual(instance.O.extract_values(), {('A3', 'B3'): 5.5, ('A1', 'B1'): 5.3, ('A2', 'B2'): 5.4})
        os.remove(currdir+'importPO.dat')


class TestTextLoad(LoadTests, unittest.TestCase):

    suffix = 'tab'


class TestCsvLoad(LoadTests, unittest.TestCase):

    suffix = 'csv'


class TestXmlLoad(LoadTests, unittest.TestCase):

    suffix = 'xml'
    skiplist = ['tableD', 'tableT', 'tableU']

    def test_tableXW_nested1(self):
        # Importing a table, but only reporting the values for the non-index
        # parameter columns.  The first column is assumed to represent an
        # index column.
        self.check_skiplist('tableXW_1')
        pyutilib.misc.setup_redirect(currdir+'importXW.dat')
        print("load "+self.filename('XW_nested1')+" query='./bar/table/*' X(A) W(A);")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.X = Param(model.A)
        model.W = Param(model.A)
        instance = model.create(currdir+'importXW.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.X.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.W.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})
        os.remove(currdir+'importXW.dat')

    def test_tableXW_nested2(self):
        # Importing a table, but only reporting the values for the non-index
        # parameter columns.  The first column is assumed to represent an
        # index column.
        self.check_skiplist('tableXW_1')
        pyutilib.misc.setup_redirect(currdir+'importXW.dat')
        print("load "+self.filename('XW_nested2')+" query='./bar/table/row' X(A) W(A);")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.X = Param(model.A)
        model.W = Param(model.A)
        instance = model.create(currdir+'importXW.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.X.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.W.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})
        os.remove(currdir+'importXW.dat')


class Spreadsheet(LoadTests):

    def filename(self, tname):
        return os.path.abspath(tutorial_dir+os.sep+self._filename)+" range="+tname+"table"


@unittest.skipIf(not xls_interface, "No XLS interface available")
class TestSpreadsheetXLS(Spreadsheet, unittest.TestCase):

    _filename='excel.xls'


@unittest.skipIf(not xlsx_interface, "No XLSX interface available")
class TestSpreadsheetXLSX(Spreadsheet, unittest.TestCase):

    _filename='excel.xlsx'


@unittest.skipIf(not xlsb_interface, "No XLSB interface available")
class TestSpreadsheetXLSB(Spreadsheet, unittest.TestCase):

    _filename='excel.xlsb'


@unittest.skipIf(not xlsm_interface, "No XLSM interface available")
class TestSpreadsheetXLSM(Spreadsheet, unittest.TestCase):

    _filename='excel.xlsm'



class TestTableCmd(unittest.TestCase):

    def test_tableA1_1(self):
        # Importing a single column of data as a set
        pyutilib.misc.setup_redirect(currdir+'importA1.dat')
        print("table columns=1 A={1} := A1 A2 A3 ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set()
        instance = model.create(currdir+'importA1.dat')
        self.assertEqual(instance.A.data(), set(['A1', 'A2', 'A3']))
        os.remove(currdir+'importA1.dat')

    def test_tableA1_2(self):
        # Importing a single column of data as a set
        pyutilib.misc.setup_redirect(currdir+'importA1.dat')
        print("table A={A} : A := A1 A2 A3 ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set()
        instance = model.create(currdir+'importA1.dat')
        self.assertEqual(instance.A.data(), set(['A1', 'A2', 'A3']))
        os.remove(currdir+'importA1.dat')

    def test_tableB1_1(self):
        # Same as test_tableA
        pyutilib.misc.setup_redirect(currdir+'importB.dat')
        print("table columns=1 B={1} := 1 2 3 ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.B = Set()
        instance = model.create(currdir+'importB.dat')
        self.assertEqual(instance.B.data(), set([1, 2, 3]))
        os.remove(currdir+'importB.dat')

    def test_tableB1_2(self):
        # Same as test_tableA
        pyutilib.misc.setup_redirect(currdir+'importB.dat')
        print("table B={B} : B := 1 2 3 ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.B = Set()
        instance = model.create(currdir+'importB.dat')
        self.assertEqual(instance.B.data(), set([1, 2, 3]))
        os.remove(currdir+'importB.dat')

    def test_tableC_1(self):
        # Importing a multi-column table, where all columns are
        # treated as values for a set with tuple values.
        pyutilib.misc.setup_redirect(currdir+'importC.dat')
        print("table columns=2 C={1,2} := A1 1 A1 2 A1 3 A2 1 A2 2 A2 3 A3 1 A3 2 A3 3 ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.C = Set(dimen=2)
        instance = model.create(currdir+'importC.dat')
        self.assertEqual(instance.C.data(), set([('A1',1), ('A1',2), ('A1',3), ('A2',1), ('A2',2), ('A2',3), ('A3',1), ('A3',2), ('A3',3)]))
        os.remove(currdir+'importC.dat')

    def test_tableC_2(self):
        # Importing a multi-column table, where all columns are
        # treated as values for a set with tuple values.
        pyutilib.misc.setup_redirect(currdir+'importC.dat')
        print("table C={a,b} : a b := A1 1 A1 2 A1 3 A2 1 A2 2 A2 3 A3 1 A3 2 A3 3 ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.C = Set(dimen=2)
        instance = model.create(currdir+'importC.dat')
        self.assertEqual(instance.C.data(), set([('A1',1), ('A1',2), ('A1',3), ('A2',1), ('A2',2), ('A2',3), ('A3',1), ('A3',2), ('A3',3)]))
        os.remove(currdir+'importC.dat')

    def test_tableZ(self):
        # Importing a single parameter
        pyutilib.misc.setup_redirect(currdir+'importZ.dat')
        print("table Z := 1.1 ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.Z = Param(default=99.0)
        instance = model.create(currdir+'importZ.dat')
        self.assertEqual(instance.Z, 1.1)
        os.remove(currdir+'importZ.dat')

    def test_tableY_1(self):
        # Same as tableXW.
        pyutilib.misc.setup_redirect(currdir+'importY.dat')
        print("table columns=2 Y(1)={2} := A1 3.3 A2 3.4 A3 3.5 ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.Y = Param(model.A)
        instance = model.create(currdir+'importY.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.Y.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        os.remove(currdir+'importY.dat')

    def test_tableY_2(self):
        # Same as tableXW.
        pyutilib.misc.setup_redirect(currdir+'importY.dat')
        print("table Y(A) : A Y := A1 3.3 A2 3.4 A3 3.5 ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.Y = Param(model.A)
        instance = model.create(currdir+'importY.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.Y.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        os.remove(currdir+'importY.dat')

    def test_tableXW_1_1(self):
        # Importing a table, but only reporting the values for the non-index
        # parameter columns.  The first column is assumed to represent an
        # index column.
        pyutilib.misc.setup_redirect(currdir+'importXW.dat')
        print("table columns=3 X(1)={2} W(1)={3} := A1 3.3 4.3 A2 3.4 4.4 A3 3.5 4.5 ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.X = Param(model.A)
        model.W = Param(model.A)
        instance = model.create(currdir+'importXW.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.X.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.W.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})
        os.remove(currdir+'importXW.dat')

    def test_tableXW_1_2(self):
        # Importing a table, but only reporting the values for the non-index
        # parameter columns.  The first column is assumed to represent an
        # index column.
        pyutilib.misc.setup_redirect(currdir+'importXW.dat')
        print("table X(A) W(A) : A X W := A1 3.3 4.3 A2 3.4 4.4 A3 3.5 4.5 ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.X = Param(model.A)
        model.W = Param(model.A)
        instance = model.create(currdir+'importXW.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.X.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.W.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})
        os.remove(currdir+'importXW.dat')

    def test_tableXW_3_1(self):
        # Like test_tableXW_1, except that set A is defined in the import statment.
        pyutilib.misc.setup_redirect(currdir+'importXW.dat')
        print("table columns=3 A={1} X(A)={2} W(A)={3} := A1 3.3 4.3 A2 3.4 4.4 A3 3.5 4.5 ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set()
        model.X = Param(model.A)
        model.W = Param(model.A)
        instance = model.create(currdir+'importXW.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3']))
        self.assertEqual(instance.X.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.W.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})
        os.remove(currdir+'importXW.dat')

    def test_tableXW_3_2(self):
        # Like test_tableXW_1, except that set A is defined in the import statment.
        pyutilib.misc.setup_redirect(currdir+'importXW.dat')
        print("table A={A} X(A) W(A) : A X W := A1 3.3 4.3 A2 3.4 4.4 A3 3.5 4.5 ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set()
        model.X = Param(model.A)
        model.W = Param(model.A)
        instance = model.create(currdir+'importXW.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3']))
        self.assertEqual(instance.X.extract_values(), {'A1':3.3,'A2':3.4,'A3':3.5})
        self.assertEqual(instance.W.extract_values(), {'A1':4.3,'A2':4.4,'A3':4.5})
        os.remove(currdir+'importXW.dat')

    def test_tableS_1(self):
        # Importing a table, but only reporting the values for the non-index
        # parameter columns.  The first column is assumed to represent an
        # index column.  A missing value is represented in the column data.
        pyutilib.misc.setup_redirect(currdir+'importS.dat')
        print("table columns=2 S(1)={2} := A1 3.3 A2 . A3 3.5 ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.S = Param(model.A)
        instance = model.create(currdir+'importS.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.S.extract_values(), {'A1':3.3,'A3':3.5})
        os.remove(currdir+'importS.dat')

    def test_tableS_2(self):
        # Importing a table, but only reporting the values for the non-index
        # parameter columns.  The first column is assumed to represent an
        # index column.  A missing value is represented in the column data.
        pyutilib.misc.setup_redirect(currdir+'importS.dat')
        print("table S(A) : A S := A1 3.3 A2 . A3 3.5 ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.A = Set(initialize=['A1','A2','A3','A4'])
        model.S = Param(model.A)
        instance = model.create(currdir+'importS.dat')
        self.assertEqual(instance.A.data(), set(['A1','A2','A3','A4']))
        self.assertEqual(instance.S.extract_values(), {'A1':3.3,'A3':3.5})
        os.remove(currdir+'importS.dat')

    def test_tablePO_1(self):
        # Importing a table that has multiple indexing columns
        pyutilib.misc.setup_redirect(currdir+'importPO.dat')
        print("table columns=4 J={1,2} P(J)={3} O(J)={4} := A1 B1 4.3 5.3 A2 B2 4.4 5.4 A3 B3 4.5 5.5 ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.J = Set(dimen=2)
        model.P = Param(model.J)
        model.O = Param(model.J)
        instance = model.create(currdir+'importPO.dat')
        self.assertEqual(instance.J.data(), set([('A3', 'B3'), ('A1', 'B1'), ('A2', 'B2')]) )
        self.assertEqual(instance.P.extract_values(), {('A3', 'B3'): 4.5, ('A1', 'B1'): 4.3, ('A2', 'B2'): 4.4} )
        self.assertEqual(instance.O.extract_values(), {('A3', 'B3'): 5.5, ('A1', 'B1'): 5.3, ('A2', 'B2'): 5.4})
        os.remove(currdir+'importPO.dat')

    def test_tablePO_2(self):
        # Importing a table that has multiple indexing columns
        pyutilib.misc.setup_redirect(currdir+'importPO.dat')
        print("table J={A,B} P(J) O(J) : A B P O := A1 B1 4.3 5.3 A2 B2 4.4 5.4 A3 B3 4.5 5.5 ;")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.J = Set(dimen=2)
        model.P = Param(model.J)
        model.O = Param(model.J)
        instance = model.create(currdir+'importPO.dat')
        self.assertEqual(instance.J.data(), set([('A3', 'B3'), ('A1', 'B1'), ('A2', 'B2')]) )
        self.assertEqual(instance.P.extract_values(), {('A3', 'B3'): 4.5, ('A1', 'B1'): 4.3, ('A2', 'B2'): 4.4} )
        self.assertEqual(instance.O.extract_values(), {('A3', 'B3'): 5.5, ('A1', 'B1'): 5.3, ('A2', 'B2'): 5.4})
        os.remove(currdir+'importPO.dat')

    def test_complex_1(self):
        # Importing a table with multiple indexing columns
        pyutilib.misc.setup_redirect(currdir+'importComplex.dat')
        print("table columns=8 I={4} J={3,5} A(J)={1} B(I)={7} :=")
        print("A1 x1 J311 I1 J321 y1 B1 z1")
        print("A2 x2 J312 I2 J322 y2 B2 z2")
        print("A3 x3 J313 I3 J323 y3 B3 z3")
        print(";")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.I = Set()
        model.J = Set(dimen=2)
        model.A = Param(model.J)
        model.B = Param(model.I)
        instance = model.create(currdir+'importComplex.dat')
        self.assertEqual(instance.J.data(), set([('J311', 'J321'), ('J312', 'J322'), ('J313', 'J323')]) )
        self.assertEqual(instance.I.data(), set(['I1', 'I2', 'I3']))
        self.assertEqual(instance.A.extract_values(), {('J311', 'J321'): 'A1', ('J312', 'J322'): 'A2', ('J313', 'J323'): 'A3'} )
        self.assertEqual(instance.B.extract_values(), {'I1': 'B1', 'I2': 'B2', 'I3': 'B3'})
        os.remove(currdir+'importComplex.dat')

    def test_complex_2(self):
        # Importing a table with multiple indexing columns
        pyutilib.misc.setup_redirect(currdir+'importComplex.dat')
        print("table I={I} J={J1,J2} A(J) B(I) :")
        print("A  x  J1   I  J2   y  B  z :=")
        print("A1 x1 J311 I1 J321 y1 B1 z1")
        print("A2 x2 J312 I2 J322 y2 B2 z2")
        print("A3 x3 J313 I3 J323 y3 B3 z3")
        print(";")
        pyutilib.misc.reset_redirect()
        model=AbstractModel()
        model.I = Set()
        model.J = Set(dimen=2)
        model.A = Param(model.J)
        model.B = Param(model.I)
        instance = model.create(currdir+'importComplex.dat')
        self.assertEqual(instance.J.data(), set([('J311', 'J321'), ('J312', 'J322'), ('J313', 'J323')]) )
        self.assertEqual(instance.I.data(), set(['I1', 'I2', 'I3']))
        self.assertEqual(instance.A.extract_values(), {('J311', 'J321'): 'A1', ('J312', 'J322'): 'A2', ('J313', 'J323'): 'A3'} )
        self.assertEqual(instance.B.extract_values(), {'I1': 'B1', 'I2': 'B2', 'I3': 'B3'})
        os.remove(currdir+'importComplex.dat')


if __name__ == "__main__":
    unittest.main()
