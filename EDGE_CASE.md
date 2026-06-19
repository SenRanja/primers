# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
get_students() should return all students, rather not hard-coded student list;
name & course must exist, and mark can be 0 defaultly (if none)
mark may not be integer, so raise an exception if not integer
mark is identitied between 0 and 100 inclusively
stats shows 0 if len(stu) is indeedly 0


2) How you have accounted for this in your implementation
Not return hard-coded student list, just return all DB students
name & course must contain valid strings, otherwise raise exception, the same with mark
Check mark value, if in plausible range
stats return None stats with necessary fileds if 0 students in DB





