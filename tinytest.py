class Test_Case():
    ''' Represents a set of input parameters. Can optionally also
        specify an expected output.

        To test the case on a function, call Test_Case.test_function(func)
    '''

    def __init__(self, params, expectation=None):
        if not isinstance(params, tuple):
            self.argc = 1
            self.params = (params, )
        else:
            self.argc = len(params)
            self.params = params

        self.expectation = expectation

    def test_function(self, func):
        ''' Tests the case on a function.
            
            return value: (Report, test_passed)
            - Report: A string which describes:
                * the test case input params
                * expected output if any
                * actual output
                * whether the case passed of failed (if applicable)
            - test_passed: A bool. Whether test passed or failed
                
        '''

        # begin building Report string
        Report = "inputs: {0}\n".format(self.params)
        if self.expectation is not None:
            Report += "expect: {0}\n".format(self.expectation)
        Report += "\n"

        # run test
        try:
            result = func(*self.params)

            # construct resultstr. resultstr looks like
            #   foo(1) == True

            # function name
            resultstr = func.__name__
            # params
            resultstr += "("
            for arg in self.params[:-1]:
                resultstr += "{}".format(arg) +", "
            resultstr += "{}".format(self.params[-1])
            resultstr += ")"
            # result
            resultstr += " == {}".format(result)

            if self.expectation is None:
                test_passed = None
            else:
                test_passed = result == self.expectation

        except TypeError as e:
            # this will happen if the number of self.params doesn't match the number of input params for func
            test_passed = False
            resultstr = "{0} RECEIVED WRONG NUMBER OF ARGUMENTS".format(
                    func.__name__)

        Report += resultstr

        if test_passed is not None:
            Report += '\n'
            if test_passed:
                Report += "PASS"
            else:
                Report += "FAIL"

        return Report, test_passed

class Test_Group():
    def __init__(self, func, cases=None):
        '''
        cases is an iterable of Test_Case
        '''
        
        # ensure func is actually a function
        if not hasattr(func, '__call__'):
            raise TypeError('First argument must be a callable!')
            
        self.func = func

        if cases is None:
            self.cases = []
        else:
            cases = list(cases)
            if cases:
                if not isinstance(cases[0], Test_Case):
                    raise ValueError("cases must contain Test_Cases")
        
        assert isinstance(self.cases, list)

    def run(self):
        all_passed = True
        result_list = []

        if len(self.cases) == 0:
            print("No test cases exist in this Test Group!")

            return result_list, all_passed
        
        print("Testing function " + self.func.__name__ + ":")
        print()
        for index, case in enumerate(self.cases):
            print("Test {} -".format(index))

            # Run test case
            case_report, case_passed = case.test_function(self.func)

            result_list.append(case_passed)
            if case_passed == False: all_passed = False
            print(case_report)
            print()

        return result_list, all_passed

def test_case_from_pair(p):
    assert len(p) == 2
    return Test_Case(*p)

def test_group_from_pairs(func, cases):
    TG = Test_Group(func, None)
    for case in cases:
        TG.cases.append(test_case_from_pair(case))

    return TG
    
