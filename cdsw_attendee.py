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
        self.Sessions = ["", "", ""]

    def Lecture_sign_in(self, day):
        if not self.Lectures[day]:
            self.Lectures[day] = True
        else:
            raise DoubleWriteException(self.EmailAddress, day)
            print(self.EmailAddress + " attempted to sign in twice!")

    def Session_sign_in(self, day, session):
        if self.Sessions[day] is "":
            self.Sessions[day] = session
        else:
            raise DoubleWriteException(self.EmailAddress, day, session)
            print(self.EmailAddress + " attempted to sign in twice!")

class MissingAttendeeException(Exception):
    """Used when a call that needs an attendee fails to locate one."""

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
