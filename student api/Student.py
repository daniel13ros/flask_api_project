class Student:
    def __init__(self,id, fname, lname, age, dept , year , birthdate ,courses):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.age = age
        self.dept = dept
        self.year = year
        self.birthdate = birthdate
        self.courses = courses
        
        
    def add_course(self, course_name):
        if course_name not in self.courses:
            self.courses.append(course_name)
            
    def edit_course(self, old_course_name, new_course_data):
        for index, course in enumerate(self.courses):
            if course['name'] == old_course_name:
                self.courses[index] = new_course_data
                return True
        return False

    def remove_course(self, course_name):
        if course_name in self.courses:
            self.courses.remove(course_name)
            
    def get_courses(self):
        return self.courses
    
    def get_gpa(self):
        sum_gpa = 0
        for course in self.courses:
            sum_gpa += course.get('grade', 0)
        return sum_gpa / len(self.courses) if self.courses else 0
            
            
            
    def update_info(self, fname=None, lname=None, age=None, dept=None, year=None, birthdate=None):
        if fname is not None:
            self.fname = fname
        if lname is not None:
            self.lname = lname
        if age is not None:
            self.age = age
        if dept is not None:
            self.dept = dept
        if year is not None:
            self.year = year
        if birthdate is not None:
            self.birthdate = birthdate
        
    def get_academic_status(self):
        gpa = self.get_gpa()
        if gpa >= 95:
            return 'Excellent'
        if gpa >= 85:
            return 'Good'
        if gpa >= 70:
            return 'Average'
        return 'Poor'
        
    def to_dict(self):
        return {
            'id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'age': self.age,
            'dept': self.dept,
            'year': self.year,
            'birthdate': self.birthdate,
            'courses': self.courses
        }