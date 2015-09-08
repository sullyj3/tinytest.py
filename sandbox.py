from mypytest import *

def lt5(i):
    if i<5:
        return True
    return False

def xor(a, b):
    if a:
        return not b
    else:
        return b

if __name__ == '__main__':
    print()
    lt5tests = [
            (1,True),
            (2,True),
            (3,True),
            (4,True),
            (5,False),
            (300, None)
    ]

    lt5_group1 = test_group_from_pairs(lt5, lt5tests)
    print(lt5_group1.run()[1])

    xortests = [
            ((True, True), False),
            ((True, False), True),
            ((False, True), True),
            ((False, False), False),
            ((True, "Hamburger"), None)
            ]

    xor_group1 = test_group_from_pairs(xor, xortests)
    print(xor_group1.run()[1])
