import gc
import os
thisdir = os.path.dirname(os.path.abspath(__file__))

import pyutilib.th as unittest

from pyomo.core import (ConcreteModel,
                        Block,
                        Param,
                        Set,
                        Var,
                        Expression,
                        Constraint,
                        Objective,
                        Reals)

class ComponentPerformanceBase(object):

    @classmethod
    def _setUpClass(self, ctype, **kwds):
        self.model = ConcreteModel()
        self.model.x = Var()
        self.model.index = Set(initialize=sorted(range(1000000)))
        self.model.del_component('test_component')
        self.model.test_component = \
            ctype(self.model.index, **kwds)

    def test_iteration(self):
        cnt = 0
        for cdata in self.model.\
            all_component_data.itervalues(self.model.test_component.type()):
            cnt += 1
        self.assertTrue(cnt > 0)
        if self.model.test_component.type() in (Set, Var):
            self.assertEqual(cnt,
                             len(self.model.test_component) + 1)
        else:
            self.assertEqual(cnt,
                             len(self.model.test_component))

@unittest.category('performance')
class TestMutableParamPerformance(unittest.TestCase,
                                  ComponentPerformanceBase):
    @classmethod
    def setUpClass(self):
        self._setUpClass(Param,
                         **{'initialize_as_dense':True,
                            'initialize':1.0,
                            'mutable':True})

@unittest.category('performance')
class TestParamPerformance(unittest.TestCase,
                           ComponentPerformanceBase):
    @classmethod
    def setUpClass(self):
        self._setUpClass(Param,
                         **{'initialize_as_dense':True,
                            'initialize':1.0,
                            'mutable':False})

@unittest.category('performance')
class TestVarPerformance(unittest.TestCase,
                         ComponentPerformanceBase):
    @classmethod
    def setUpClass(self):
        self._setUpClass(Var, **{'initialize':1.0})

@unittest.category('performance')
class TestVarMultiDomainPerformance(unittest.TestCase,
                                    ComponentPerformanceBase):
    @classmethod
    def setUpClass(self):
        self._setUpClass(Var,
                         **{'domain': lambda m,i: Reals})

@unittest.category('performance')
class TestExpressionPerformance(unittest.TestCase,
                                    ComponentPerformanceBase):
    @classmethod
    def setUpClass(self):
        self._setUpClass(Expression,
                         **{'initialize': 1.0})

@unittest.category('performance')
class TestConstraintPerformance(unittest.TestCase,
                                    ComponentPerformanceBase):
    @classmethod
    def setUpClass(self):
        self._setUpClass(Constraint,
                         **{'rule': lambda m,i: 1 <= m.x <= 2})

@unittest.category('performance')
class TestObjectivePerformance(unittest.TestCase,
                               ComponentPerformanceBase):
    @classmethod
    def setUpClass(self):
        self._setUpClass(Objective,
                         **{'rule': lambda m,i: m.x})

@unittest.category('performance')
class TestSetPerformance(unittest.TestCase,
                         ComponentPerformanceBase):
    @classmethod
    def setUpClass(self):
        self._setUpClass(Set,
                         **{'initialize': [1,2,3]})

@unittest.category('performance')
class TestBlockPerformance(unittest.TestCase,
                           ComponentPerformanceBase):
    @classmethod
    def setUpClass(self):
        self._setUpClass(Block, **{'rule': lambda b,i: b})

    def test_all_blocks(self):
        cnt = 0
        for block in self.model.all_blocks():
            cnt += 1
        self.assertTrue(cnt > 0)
        self.assertEqual(cnt,
                         len(self.model.test_component) + 1)

if __name__ == "__main__":
    unittest.main()


