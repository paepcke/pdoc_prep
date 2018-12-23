'''
Created on Dec 20, 2018

@author: paepcke
'''
from _io import StringIO
import unittest
from unittest import skipIf

from pdoc_post_prod.pdoc_post_prod import PdocPostProd 
from pdoc_post_prod.pdoc_post_prod import NoParamError, NoTypeError, ParamTypeMismatch

RUN_ALL = True
#RUN_ALL = False

class TestPdocPostProd(unittest.TestCase):

    content_good = \
    '''Foo is bar
       :param tableName: name of new table
       :type tableName: String
       Blue is green
       '''
    content_long_parm_line = \
    '''Foo is bar
       :param tableName: name of new table
           that I created just for you.       
       :type tableName: String
       Blue is green
       '''
    content_no_type = \
    '''Foo is bar
       :param tableName: name of new table
       Blue is green
       '''
    content_no_param = \
    '''Foo is bar
       :type tableName: String
       Blue is green
       '''
    
    content_param_type_mismatch = \
    '''Foo is bar
       :param tableName: name of new table
       :type bluebell: String
       Blue is green
       '''
    content_return_variationA = \
    '''Foo is bar
       :return a number between 1 and 10
       Blue is green
       '''
    content_return_variationB = \
    '''Foo is bar
       :returns a number between 1 and 10
       Blue is green
       '''
    content_return_variationC = \
    '''Foo is bar
       :return: a number between 1 and 10
       Blue is green
       '''
    content_return_variationD = \
    '''Foo is bar
       :returns: a number between 1 and 10
       Blue is green
       '''
    content_rtype_variationA = \
    '''Foo is bar
       :rtype {int | str}
       Blue is green
       '''
    content_rtype_variationB = \
    '''Foo is bar
       :rtype: {int | str}
       Blue is green
       '''    
    
    content_raises_variationA = \
    '''Foo is bar
       :raises ValueError
       Blue is green
       '''
    content_raises_variationB = \
    '''Foo is bar
       :raises: ValueError
       Blue is green
       '''    
    
    #-------------------------
    # setUp 
    #--------------

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.capture_stream = StringIO()

    #-------------------------
    # testParamAndTypeAllOK
    #--------------

    @skipIf(not RUN_ALL, 'Temporarily disabled')
    def testParamAndTypeAllOK(self):
        for delimiter_char in [':', '@']:
            adjusted_content = self.set_delimiter_char(TestPdocPostProd.content_good, delimiter_char)
            in_stream      = StringIO(adjusted_content)
            PdocPostProd(in_stream, self.capture_stream, delimiter_char=delimiter_char)
            
            res = self.capture_stream.getvalue()
            expected = 'Foo is bar\n' +\
                       '       <b>tableName</b> (<b></i>String</i></b>): name of new table</br>' +\
                       '       Blue is green\n'
            self.assertEqual(res, expected)
            # Clean out the capture stream:
            self.capture_stream = StringIO()
    #-------------------------
    # testParamMultiline
    #--------------

    @skipIf(not RUN_ALL, 'Temporarily disabled')
    def testParamMultiline(self):
        for delimiter_char in [':', '@']:
            adjusted_content = self.set_delimiter_char(TestPdocPostProd.content_long_parm_line, delimiter_char)
            in_stream      = StringIO(adjusted_content)
            PdocPostProd(in_stream, self.capture_stream, delimiter_char=delimiter_char)
             
            res = self.capture_stream.getvalue()
            expected = 'Foo is bar\n' +\
                       '       <b>tableName</b> (<b></i>String</i></b>): name of new table            that I created just for you.       \n</br>' +\
                       '       Blue is green\n'            
            self.assertEqual(res, expected)
            # Clean out the capture stream:
            self.capture_stream = StringIO()

      
    #-------------------------
    # testParamNoTypeForceWithTypeMissing 
    #--------------
        
    @skipIf(not RUN_ALL, 'Temporarily disabled')
    def testParamNoTypeForceWithTypeMissing(self):
        for delimiter_char in [':', '@']:
            adjusted_content = self.set_delimiter_char(TestPdocPostProd.content_no_type, delimiter_char)
            in_stream = StringIO(adjusted_content)
            PdocPostProd(in_stream,
                         self.capture_stream, 
                         delimiter_char=delimiter_char,
                         force_type_spec=False)
            res = self.capture_stream.getvalue()
            expected = 'Foo is bar\n       <b>tableName</b> name of new table        Blue is green</br>'
            self.assertEqual(res, expected)
            # Clean out the capture stream:
            self.capture_stream = StringIO()            

    #-------------------------
    # testParamWithTypeMissing 
    #--------------
        
    @skipIf(not RUN_ALL, 'Temporarily disabled')
    def testParamWithTypeMissing(self):
        for delimiter_char in [':', '@']:
            adjusted_content = self.set_delimiter_char(TestPdocPostProd.content_no_type, delimiter_char)
            in_stream = StringIO(adjusted_content)
            with self.assertRaises(NoTypeError):
                PdocPostProd(in_stream,
                             self.capture_stream, 
                             delimiter_char=delimiter_char,
                             force_type_spec=True)

    #-------------------------
    # testTypeWithParamMissing 
    #--------------

    @skipIf(not RUN_ALL, 'Temporarily disabled')
    def testTypeWithParamMissing(self):
        for delimiter_char in [':', '@']:
            adjusted_content = self.set_delimiter_char(TestPdocPostProd.content_no_param, delimiter_char)
            in_stream = StringIO(adjusted_content)
            with self.assertRaises(NoParamError):
                PdocPostProd(in_stream, self.capture_stream, delimiter_char=delimiter_char)
        
    #-------------------------
    # testParamTypeMismatch 
    #--------------
        
    @skipIf(not RUN_ALL, 'Temporarily disabled')        
    def testParamTypeMismatch(self):
        for delimiter_char in [':', '@']:
            adjusted_content = self.set_delimiter_char(TestPdocPostProd.content_param_type_mismatch, delimiter_char)
            in_stream = StringIO(adjusted_content)
            with self.assertRaises(ParamTypeMismatch):
                PdocPostProd(in_stream, self.capture_stream, delimiter_char=delimiter_char)
        
    #-------------------------
    # testReturnSpec 
    #--------------
    
    @skipIf(not RUN_ALL, 'Temporarily disabled')
    def testReturnSpec(self):
        for delimiter_char in [':', '@']:
            for _input in [TestPdocPostProd.content_return_variationA,
                           TestPdocPostProd.content_return_variationB,
                           TestPdocPostProd.content_return_variationC,
                           TestPdocPostProd.content_return_variationD
                           ]:
                adjusted_content = self.set_delimiter_char(_input, delimiter_char)
                in_stream        = StringIO(adjusted_content)
                PdocPostProd(in_stream, self.capture_stream, delimiter_char=delimiter_char)
                
                res = self.capture_stream.getvalue()
                expected = 'Foo is bar\n' +\
                           '       <b>returns:</b> a number between 1 and 10' +\
                           ' Blue is green</br>'
                self.assertEqual(res, expected)
                # Make a new capture stream so the old
                # content won't confuse us on the next loop:
                self.capture_stream = StringIO()
        
    #-------------------------
    # testRtypeSpec 
    #--------------
    
    @skipIf(not RUN_ALL, 'Temporarily disabled')
    def testRtypeSpec(self):
        for delimiter_char in [':', '@']:
            for _input in [TestPdocPostProd.content_rtype_variationA,
                           TestPdocPostProd.content_rtype_variationB
                           ]:
                adjusted_content = self.set_delimiter_char(_input, delimiter_char)
                in_stream      = StringIO(adjusted_content)
                PdocPostProd(in_stream, self.capture_stream, delimiter_char=delimiter_char)
                
                res = self.capture_stream.getvalue()
                expected = 'Foo is bar\n' +\
                           '       <b>return type:</b> {int | str}</br>' +\
                           '       Blue is green\n'
                self.assertEqual(res, expected)
                # Make a new capture stream so the old
                # content won't confuse us on the next loop:
                self.capture_stream = StringIO()
    
    #-------------------------
    # testRaisesSpec 
    #--------------
        
    @skipIf(not RUN_ALL, 'Temporarily disabled')
    def testRaisesSpec(self):
        for delimiter_char in [':', '@']:
        
            for _input in [TestPdocPostProd.content_raises_variationA,
                           TestPdocPostProd.content_raises_variationB
                           ]:
                adjusted_content = self.set_delimiter_char(_input, delimiter_char)
                in_stream      = StringIO(adjusted_content)
                PdocPostProd(in_stream, self.capture_stream, delimiter_char=delimiter_char)
                
                res = self.capture_stream.getvalue()
                expected = 'Foo is bar\n' +\
                           '       <b>raises:</b> ValueError</br>' +\
                           '       Blue is green\n'
                self.assertEqual(res, expected)
                # Make a new capture stream so the old
                # content won't confuse us on the next loop:
                self.capture_stream = StringIO()
        
    #-------------------------
    # set_delimiter_char 
    #--------------
    
    def set_delimiter_char(self, content, delimiter_char):
        '''
        Given one of the test input strings and a 
        delimiter char (':' or '@'), return a new
        content string that uses the given delimiter
        char in all the lines that contain directives.
        
        @param content: content to be passed into PdocPostProd
            instance for testing.
        @type content: str
        @param delimiter_char: the delimiter char to use in the
            new content string. One of ':' and '@'.
        @type delimiter_char: char
        '''
        new_content = content.replace(':param', delimiter_char+'param')
        new_content = new_content.replace(':type', delimiter_char+'type')
        new_content = new_content.replace(':return', delimiter_char+'return')
        new_content = new_content.replace(':rtype', delimiter_char+'rtype')
        new_content = new_content.replace(':raises', delimiter_char+'raises')
        return new_content
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()