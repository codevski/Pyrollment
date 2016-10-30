import os
import unittest
import tempfile
import shutil

"""
A system that managers enrolments for tutorial classes. Written in Python 
and to be used by students, tutors and administrative staff.

"""

def read_lines(filename):
    """This is read_lines utility
    It reads lines and returns a LIST"""
    if os.path.exists(filename):
        L = []
        for line in open(filename, "r").readlines():
            li = line.strip()
            if not li.startswith("#"):
                # Removes \n and \r (If it was used in windows)
                newline = line.strip('\n\r')
                L.append(newline)
        return L
    else:
        return 0
    
def read_table(filename):
    """This is read_table utility
    In this module lines are being passed to read_lines"""
    if os.path.exists(filename):
        L = []
        for line in read_lines(filename):
            newline = line.split(':')
            L.append(newline)
    
        return L
    else:
        return 0


def write_lines(filename, lines):
    """ This is the write_lines utility
    In this utility it creates tempoarary file and if write is 
    successful it removes original file and renames temp file to the 
    original file"""
    try:
        tmpFile = tempfile.NamedTemporaryFile(mode='w+r', delete=False)
        for line in lines:
            tmpFile.write(line + '\n')
        tmpFile.close()
        # There seem to be a issue with tmp file located on another dir tree.
        # Works locally using 2.6 and works on a remote server running 2.6.
        os.rename(tmpFile.name, filename)
        return 1
    except:
            return 0

class Enrol(object):
    """This is the main Enrol Class"""
    def __init__(self, data_path=None):
        """ Accepts one argument which is the path to the data
        directory."""
        self.data_path = data_path
        if not os.path.exists(data_path):
            raise IOError("Path doesn't exist!")
        # Loads all data into memory
        self.subjects_table = read_table(os.path.join(data_path, 'SUBJECTS'))
        self.classes_table = read_table(os.path.join(data_path, 'CLASSES'))
        self.venues_table = read_table(os.path.join(data_path, 'VENUES'))

    def subjects(self):
        """Accepts no arguments. Returns a list of all subject codes
        in the enrollment system"""
        x = 0
        alist = []
        subjects = self.subjects_table
        # Creating new list with just subject
        for _ in subjects:
            x+=1
            alist.append(subjects[x-1][0])
        return alist

    def subject_name(self, name):
        """Accepts one argument of subject code. Returns a string which
        is the name of the specified subject. Raises KeyError if the 
        specified subject code does not exist"""
        adic = {}
        key = name
        subjects = self.subjects_table
        for subcode, title in subjects:
            if subcode == name:
                adic.setdefault(key, [])
                adic[key].append(title)
        try:
            title = ', '.join(adic[key])
            return title
        except KeyError:
            raise KeyError('Class Code Not Found')

    def classes(self, names):
        """Accepts one argument of subject code. Returns a list of class 
        codes for the specified subject in no order. Raises KeyError 
        if subject code not found."""
        adic = {}
        eclasses = self.classes_table
        key = names
        for classcode, subcode, _, _, _ in eclasses:
            if subcode == names:
                adic.setdefault(key, [])
                adic[key].append(classcode)
        
        try:
            return adic[key]
        except KeyError:
            raise KeyError('Class Code Not Found')

    def class_info(self, names):
        """Accepts one argument of class. Returns class info in a tuple.
        Raises a KeyError if specified class code does not exist"""
        alist = []
        atuple = ()
        adic = {}
        eclassess = self.classes_table
        sroll = read_lines(os.path.join(self.data_path, names+".roll"))
        key = names
        for classcode, subcode, cdate, croom, teacher in eclassess:
            if classcode == names:
                alist = [classcode, subcode, cdate, croom, teacher]
                alist.append(sroll)
                atuple = tuple(alist)
                adic.setdefault(key, [])                
        try:
            adic[key].append(atuple)
            return atuple
        except KeyError:
            raise KeyError('Class Code Not Found')

    def check_student(self, studid, subcode=None):
        """Accepts one or two arguments. First required argument is a 
        student ID (String). The second is optional argument of a subject 
        code. If subject code specified, returns the class codes of the 
        student he or she is enrolled in. If student does not exist or 
        no subject code found returns None."""
        if subcode != None:
            try:
                theclasses = self.classes(subcode)
            except:
                return None
            for checkstud in theclasses:
                thelist = list(self.class_info(checkstud))
            if isinstance(thelist, list):
                if thelist[5] == 0:
                    pass
                else:   
                    students = thelist[5][0:]
                    if studid in students:
                        return thelist[0]
        else:
            L = []
            allsubjects = self.subjects()
            for asubject in allsubjects:
                theclasses = self.classes(asubject)
                for checkstud in theclasses:
                    thelist = list(self.class_info(checkstud))
                    if isinstance(thelist[5], list):
                        if thelist[5] == 0:
                            pass
                        else:
                            students = thelist[5][0:]
                            if studid in students:
                                L.append(thelist[0])
            return L

    def enrol(self, studentID, classCode):
        """Accepts two arguments. Student ID and a class Code. Returns 1 
        if successful. None if failed."""
        rollfile = read_lines(os.path.join(self.data_path, classCode+".roll"))
        if isinstance(rollfile, int):
            sizeofclass = 0
        else:
            sizeofclass = self._getClassSize(classCode)
        classSize = self._getVenueSpace(classCode)
        if int(sizeofclass) < int(classSize):
            varclassinfo = [self.class_info(classCode)]
            for _, varsubject, _, _, _, _ in varclassinfo:
                foundsubject = varsubject
            varclasses = self.check_student(studentID, foundsubject)
            if varclasses != None:
                classlist = read_lines(os.path.join(self.data_path, 
                                                    classCode+'.roll'))
                classlist.remove(studentID)
                classlist.append(studentID)
                return write_lines(os.path.join(self.data_path, 
                                                classCode+'.roll'), classlist)
            else:
                return write_lines(os.path.join(
                            self.data_path, classCode+'.roll'), [studentID])
        else:
            return None

    def _getVenueSpace(self,class_code):
        """Returns the total venue space with the given class_code"""
        try:
            classinfo = self.class_info(class_code)
            venues = self.venues_table
            for i in range(0,len(venues)):
                if classinfo[3] in venues[i]:
                    cap = venues[i][1]
            return cap
        except KeyError:
            raise KeyError('Class Code Not Found')
    
    def _getClassSize(self, class_code, SubjectCode=None):
        """Returns the class size. Accepts two arguments, first class code 
        and second optional subject code"""
        try:
            classSize = len(read_lines(os.path.join(self.data_path, 
                                                    class_code+'.roll')))
            return classSize
        except:
            return 0
            
class EnrolTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp() 
        self.filelist = open(self.dir+'/testfile', 'w+r')
        self.filelist.writelines(['test\n','test2\n'])
        self.filelist.close()
           
        # SUBJECTS
        self.subjectfile = open(os.path.join(self.dir, 'SUBJECTS'), 'w+r')
        self.subjectfile.writelines(['scr101:Intro to Scaring\n', 
                                     'scr102:History of Scaring\n', 
                                     'scr202:Disappearing & Hiding\n'])
        self.subjectfile.close()
           
        # CLASSES
        self.classesfile = open(os.path.join(self.dir, 'CLASSES'), 'w+r')
        self.classesfile.writelines(
                            ['scr101.1:scr101:Mon 9.30:2.5.10:Dr. Sullivan\n', 
                            'scr102.1:scr102:Tue 14.30:2.6.1:Prof. Wazowski\n', 
                            'scr102.2:scr102:Wed 14.30:2.6.1:Prof. Wazowski\n', 
                            'scr202A:scr202:Tue 15.30:23.5.32:Randy II\n'])
        self.classesfile.close()
           
        # VENUES
        self.venuefile = open(os.path.join(self.dir, 'VENUES'), 'w+r')
        self.venuefile.writelines(['2.5.10:18\n', 'Lab 2:8\n', '2.6.1:22\n', 
                                   '23.5.32:1'])
        self.venuefile.close()
           
        # Class Roll 1
        self.rollfile1 = open(os.path.join(self.dir, 'scr101.1.roll'), 'w+r')
        self.rollfile1.writelines(['s3435996'])
        self.rollfile1.close()
         
        # Class Roll 2
        self.rollfile1 = open(os.path.join(self.dir, 'scr202A.roll'), 'w+r')
        self.rollfile1.writelines(['s34359966'])
        self.rollfile1.close()
        pass
              
    def test_read_lines(self):
        # assertIsInstance == List would be better option.
        self.assertTrue(read_lines(os.path.join(self.dir, 'SUBJECTS')), 
            ['scr101:Intro to Scaring', 'scr102:History of Scaring', 
             'scr202:Disappearing & Hiding'])
        pass
             
    def test_read_table(self):
        # assertIsInstance == List would be better option.
        self.assertTrue(read_lines(os.path.join(self.dir, 'SUBJECTS')), 
            ['scr101:Intro to Scaring', 'scr102:History of Scaring', 
             'scr202:Disappearing & Hiding'])
        pass
             
    def test_write_lines(self):
        # assertIsInstance == Int would be better option.
        testfile = os.path.join(self.dir, 'TESTWRITE')
        self.assertTrue(write_lines(testfile,('test\n')), 1)
        pass
             
    def test_subjects(self):
        e = Enrol(self.dir)
        Subjects = e.subjects()
        self.assertTrue(e.subjects(), Subjects)
        pass
         
    def test_subject_name(self):
        e = Enrol(self.dir)
        # Test if incorrect subject name is passed with KeyError catch
        self.assertRaises(KeyError,e.subject_name, 'scr1011')
        pass
         
    def test_classes(self):
        e = Enrol(self.dir)
        # Checks 
        self.assertTrue(e.classes("scr101"), ["scr101.1"])
        self.assertRaises(KeyError,e.classes, 'scr1011')
        pass
         
    def test_class_info(self):
        e = Enrol(self.dir)
        self.assertTrue(e.class_info("scr101.1"), 
                        ('scr101.1:scr101:Mon 9.30:2.5.10:Dr. Sullivan'))
        self.assertRaises(KeyError,e.class_info, 'scr1011')
        pass
         
    def test_check_student(self):
        e = Enrol(self.dir)
        self.assertEqual(e.check_student('s3435996'), ['scr101.1'])
        self.assertTrue(e.check_student('s3435996'), None)
        pass
         
    def test_enrol(self):
        e = Enrol(self.dir)
        self.assertEqual(e.enrol('s34359966', 'scr101.1'), 1)
        self.assertEqual(e.enrol('s34359966', 'scr202A'), None)
        self.assertRaises(KeyError,e.enrol, 's34359966', 'scr1012111')     
        pass
         
    # All tests had assertIsInstance. Not included in 2.6
    def tearDown(self):
        shutil.rmtree(self.dir)
        pass     
         
if __name__ == '__main__':
    unittest.main()

