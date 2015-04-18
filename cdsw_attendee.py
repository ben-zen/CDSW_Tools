# Copyright (C) 2015 Ben Lewis

class DoubleWriteException(Exception):
    def __init__(self, email, day, session = None):
        self.EmailAddress = email
        self.Day = day
        if session is not None:
            self.Session = session

class Attendee:
    """A log of an attendee's presence at various elements of the CDSW."""

    def __init__(self, email):
        self.EmailAddress = email
        self.Lectures = [False, False, False, False]
        self.Sessions = ["", "", "", ""]

    def Lecture_sign_in(self, day):
        if not self.Lectures[day]:
            self.Lectures[day] = True
        else:
            raise DoubleWriteException(self.EmailAddress, day)

    def Session_sign_in(self, day, session):
        if self.Sessions[day] is "":
            self.Sessions[day] = session
        else:
            raise DoubleWriteException(self.EmailAddress, day, session)

class MissingAttendeeException(Exception):
    """Used when a call that needs an attendee fails to locate one."""

    def __init__(self, email):
        self.EmailAddress = email

class PreexistingAttendeeException(Exception):
    """Represents attempting to create an attendee that already exists."""

    def __init__(self, email):
        self.EmailAddress = email

class Workshop:

    def __init__(self):
        self.Attendees = {}

    def Find_attendee(self, email):
        if email in self.Attendees:
            return self.Attendees[email]
        else:
            raise MissingAttendeeException(email)

    def Add_attendee(self, email):
        if email not in self.Attendees:
            self.Attendees[email] = Attendee(email)
        else:
            raise PreexistingAttendeeException(email)

    def Show_attendance_by_session(self, day):
        sessions = {}
        for x in self.Attendees.values():
            if x.Sessions[day] in sessions:
                sessions[x.Sessions[day]] = sessions[x.Sessions[day]] + 1
            else:
                sessions[x.Sessions[day]] = 1
        return sessions
