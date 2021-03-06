from flask import Blueprint, jsonify, request
from . import models
from backend import db
from cruds.crud_users.models import Users
from cruds.crud_course_sections.models import CourseSections
import datetime
from sqlalchemy import and_
from cruds.crud_student_attendance.models import StudentAttendance
from cruds.crud_course_section_students.models import CourseSectionStudents
import pdb


section_times = Blueprint("section_times", __name__)


@section_times.route('/section_time_in_progress/<teacher_id>', methods=['GET'])
def section_time_in_progress(teacher_id):
    # Docs
    """
           Section Time in Progress
           ---
           tags:
             - /section_times
           responses:
             200:
               description:  This is the service to get the section time in progress to the teacher id
               schema:
                 properties:
                   section_times:
                     type: array
                     description: Section Times list
                     items:
                       type: string
                       default: { "course_section": {
                                                        "code": string,
                                                        "course": {
                                                          "code": string,
                                                          "id": integer,
                                                          "name": string
                                                        },
                                                        "id": 1,
                                                        "name": string,
                                                        "teacher_id": integer
                                                      },
                                                      "id": 1,
                                                      "section_time_finish_time": "HH:MM:SS",
                                                      "section_time_start_time": "HH:MM:SS",
                                                      "week_day": integer}
    """

    section_times = (db.session.query(models.SectionTimes).filter(Users.id == CourseSections.teacher_id).
                       filter(CourseSections.id == models.SectionTimes.course_section_id).
                       filter(Users.id == teacher_id).all())
    return jsonify(section_times=[section_time.serialize() for section_time in section_times])


@section_times.route('/student_attendance_register/<section_time_id>', methods=['POST'])
def student_attendance_register(section_time_id):
    # Docs
    """
           Register of the Student Attendance
           ---
           tags:
             - /section_times
           responses:
             200:
               description:  This is the service to add a new section time in the course section.
               schema:
                 properties:
                   course_section:
                     type: array
                     description: Course Sections list
                     items:
                       type: string
                       default: {"id": integer, "code": string, "name": string, "course": { "code": string, "id": integer, "name": string }, "teacher_id": integer}
    """

    student_attendance_list = request.get_json()['student_attendance']
    section_time_date = request.get_json()['section_time_date']

    section_time = models.SectionTimes.query.get(section_time_id)
    student_attendance_registered = StudentAttendance.query.filter_by(section_time_id=section_time_id).all()

    if not student_attendance_registered:
        course_section_id = section_time.course_section_id
        try:
            with db.session.no_autoflush:
                for register in student_attendance_list:
                    student_attendance = StudentAttendance(status=register['status'], section_time_date=datetime.datetime.strptime(section_time_date, "%m-%d-%Y").date())
                    student_attendance.course_section_student_id = CourseSectionStudents.query.filter_by(user_id=register['student_id'],course_section_id=course_section_id).first().id
                    section_time.student_attendance.append(student_attendance)

            db.session.commit()
            return jsonify(student_attendance=[student_attendance.serialize() for student_attendance in
                                               section_time.student_attendance]), 200
        except:
            return jsonify(result="Invalid request"), 404
    return jsonify(result="Section time already registered"), 400

@section_times.route('/update_section_time/<section_time_id>', methods=['POST'])
def update_section_time(section_time_id):
    section_time = models.SectionTimes.query.get(section_time_id)

    if section_time:
        section_time.set_fields(dict(request.form.items()))
        db.session.commit()
        return jsonify(section_time=[section_time.serialize() for section_time in models.SectionTimes.query.filter_by(id=section_time_id)])
    return jsonify(result='invalid section time id')