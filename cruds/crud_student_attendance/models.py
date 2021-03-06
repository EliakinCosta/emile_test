from backend import db
import datetime
from cruds.crud_users.models import Users
from cruds.crud_course_section_students.models import CourseSectionStudents


class StudentAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_time_id = db.Column(db.Integer, db.ForeignKey('section_times.id'))
    course_section_student_id = db.Column(db.Integer, db.ForeignKey('course_section_students.id'))
    status = db.Column(db.String(1))
    section_time_date = db.Column(db.Date())
    course_section_student = db.relationship("CourseSectionStudents")

    def serialize(self):
        return {
            'id': self.id,
            'section_time_id': self.section_time_id,
            'course_section_student_id': self.course_section_student_id,
            'status': self.status,
            'section_time_date':  datetime.date.strftime(self.section_time_date, "%m-%d-%Y")
        }


