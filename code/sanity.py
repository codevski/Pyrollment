#!/usr/bin/env python
import inspect, sys

try:
    import enrol
except ImportError:
    print '-' * 60
    print 'Error: unable to import the enrol module.'
    print 'Is your enrol.py in the same directory and named correctly?'
    print '-' * 60
    sys.exit(-1)

print 'Check module functions:'

print '  - enrol module contains function read_lines() that accepts 1 arg'
assert 'read_lines' in dir(enrol) and callable(enrol.read_lines) and enrol.read_lines.func_code.co_argcount == 1

print '  - enrol module contains function read_table() that accepts 1 arg'
assert 'read_table' in dir(enrol) and callable(enrol.read_table) and enrol.read_table.func_code.co_argcount == 1

print '  - enrol module contains function write_lines() that accepts 2 args'
assert 'write_lines' in dir(enrol) and callable(enrol.write_lines) and enrol.write_lines.func_code.co_argcount == 2

print '\nCheck Enrol class and its methods:'

print '  - enrol module contains class Enrol'
assert 'Enrol' in dir(enrol) and inspect.isclass(enrol.Enrol)

print '  - Enrol class contains a constructor that accepts 1 arg (other than self)'
assert '__init__' in dir(enrol.Enrol) and callable(enrol.Enrol.__init__) and enrol.Enrol.__init__.func_code.co_argcount == 2

print '  - Enrol class contains method subjects() that accepts no arg (other than self)'
assert 'subjects' in dir(enrol.Enrol) and callable(enrol.Enrol.subjects) and enrol.Enrol.subjects.func_code.co_argcount == 1

print '  - Enrol class contains method subject_name() that accepts 1 arg (other than self)'
assert 'subject_name' in dir(enrol.Enrol) and callable(enrol.Enrol.subject_name) and enrol.Enrol.subject_name.func_code.co_argcount == 2

print '  - Enrol class contains method classes() that accepts 1 arg (other than self)'
assert 'classes' in dir(enrol.Enrol) and callable(enrol.Enrol.classes) and enrol.Enrol.classes.func_code.co_argcount == 2

print '  - Enrol class contains method class_info() that accepts 1 arg (other than self)'
assert 'class_info' in dir(enrol.Enrol) and callable(enrol.Enrol.class_info) and enrol.Enrol.class_info.func_code.co_argcount == 2

print '  - Enrol class contains method check_student() that accepts 1 or 2 args (other than self)'
assert 'check_student' in dir(enrol.Enrol) and callable(enrol.Enrol.check_student) and enrol.Enrol.check_student.func_code.co_argcount == 3 and len(inspect.getargspec(enrol.Enrol.check_student).defaults) == 1

print '  - Enrol class contains method enrol() that accepts 2 args (other than self)'
assert 'enrol' in dir(enrol.Enrol) and callable(enrol.Enrol.enrol) and enrol.Enrol.enrol.func_code.co_argcount == 3

print '\n### Check completed with no errors.'
print '### Your enrol module should be compatible with the marking script.'
print '### This sanity check does NOT test any functionality.'
print '### Your unit tests should verify the functional requirements.'
