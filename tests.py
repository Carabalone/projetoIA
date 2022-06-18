import unittest as ut
import takuzu as tz

class TestBoard(ut.TestCase):
    def testIn(self):
        bd = tz.Board([[2,2,1,1],[1,0,2,1],[0,2,1,0],[1,2,1,2]])
        self.assertTrue(type(bd == tz.Board))
        self.assertTrue(2 in bd)
        self.assertTrue(1 in bd)
        self.assertTrue(0 in bd)
    def testCols(self):
        bd = tz.Board([[1,1,1,1],[1,1,1,1],
                        [0,2,1,0],[1,2,1,2]])
        self.assertTrue(bd.check_lines() == False)
        #self.assertTrue(bd.check_row_and_col() == False)
        bd = tz.Board([[1,1,1,1],[1,0,1,1],
                        [1,2,1,0],[1,2,1,2]])
        self.assertTrue(bd.check_cols() == False)
        #self.assertTrue(bd.checkrow_and_col() == False)
        bd = tz.Board([[2,2,1,1],[1,0,2,1],[0,2,1,0],[1,2,1,2]])
        self.assertTrue(bd.check_cols() == True)
        self.assertTrue(bd.check_lines() == True)
        #self.assertTrue(bd.check_row_and_col() == True)
    def testOverHalf(self):
        bd = tz.Board([[1,1,1,1],[1,1,1,1],
                        [0,2,1,0],[0,2,1,2]])
        self.assertTrue(bd.check_over_half() == False)
        bd = tz.Board([[1,1,0,0],[1,1,0,0],
                        [0,2,1,0],[1,2,1,2]])
        self.assertTrue(bd.check_over_half() == False)
        bd = tz.Board([[1,1,0,0],
                       [1,1,0,0],
                       [0,0,1,1],
                       [0,0,1,1]])
        self.assertTrue(bd.check_over_half() == True)
        bd = tz.Board([[2,1,0,0],[2,1,0,0],
                    [2,0,1,1],[2,0,1,1]])
        self.assertTrue(bd.check_over_half() == True)
        bd = tz.Board([[1,1,0,0],[2,2,2,2],
                    [2,0,1,1],[2,0,1,1]])
        self.assertTrue(bd.check_over_half() == True)
    
    def testZeroOnePair(self):
        bd = tz.Board([[1,1,1,1],[1,1,1,1],
                        [0,2,1,0],[0,2,1,2]])
        self.assertFalse(bd.check_zero_one())
        bd = tz.Board([[0,0,1,1],[0,0,1,1],
                        [0,0,1,1],[0,0,1,1]])
        self.assertFalse(bd.check_zero_one())
        bd = tz.Board([[0,1,0,1],
                       [1,0,1,0],
                       [0,1,0,1],
                       [1,0,1,0]])
        self.assertTrue(bd.check_zero_one())
        bd = tz.Board([[0,1,2,1],
                       [1,0,1,0],
                       [0,1,0,1],
                       [1,0,1,0]])
        self.assertRaises(ValueError, bd.check_zero_one)

    def testZeroOneOdd(self):
        bd = tz.Board([[1,1,1,0,1],[1,1,1,1,1],
                        [0,2,1,0,1],[0,2,1,2,1], [0,0,1,1,0]])
        self.assertFalse(bd.check_zero_one())
        bd = tz.Board([[0,0,1,1],[0,0,1,1],
                        [0,0,1,1],[0,0,1,1], [1,0,1,1]])
        self.assertFalse(bd.check_zero_one())
        bd = tz.Board([[0,1,0,1,1],
                       [1,0,1,0,1],
                       [0,1,0,1,1],
                       [1,0,1,0,0],
                       [1,0,1,0,0]])
        self.assertTrue(bd.check_zero_one())
        bd = tz.Board([[0,1,2,1,1],
                       [1,0,1,1,0],
                       [0,1,0,1,1],
                       [1,0,1,0,1],
                       [1,0,1,0,1]])
        self.assertRaises(ValueError, bd.check_zero_one)

        


if __name__ == "__main__":
    ut.main()