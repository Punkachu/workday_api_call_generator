import unittest

from test_get_journals import TestXMLJournalParsing


def suite():
    suite = unittest.TestSuite()
    # suite.addTest(unittest.makeSuite(TestAccountingDates))
    # suite.addTest(unittest.makeSuite(TestXMLParsing))
    suite.addTest(unittest.makeSuite(TestXMLJournalParsing))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
