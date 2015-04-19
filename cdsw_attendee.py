# Copyright (C) 2015 Ben Lewis
# Licensed under the MIT license.

class DoubleWriteException(Exception):
    """Thrown when a second write is attempted to the same item in one of an
    Attendee object's lists.

    Members:
    EmailAddress -- Identifier of the throwing Attendee
    Day          -- Day of the workshop which the duplicate write was attempting
    Session      -- Optional argument.  If this is not `None`, the session field
                    for that day was being written to.  If it is `None`, then a
                    second checkin was attempted.
    """

    def __init__(self, email, day, session = None):
        self.EmailAddress = email
        self.Day = day
        if session is not None:
            self.Session = session

class Attendee:
    """A log of an attendee's presence at various elements of the CDSW.

    Members:
    EmailAddress -- a unique identifier for each CDSW attendee
    Lectures     -- an array of 4 booleans, each one representing attendace at a
                    lecture; the setup night is considered Lecture 0.
    Sessions     -- an array of 4 strings; for the Seattle CDSW, we leave the
                    first blank.  These are used for storing which afternoon
                    session each attendee went to, based on their reporting.
    """

    def __init__(self, email):
        """Setup method for the Attendee object.

        Keyword arguments:
        email -- The identifier for the attendee, for lookup and comparison.
        """
        self.EmailAddress = email
        self.Lectures = [False, False, False, False]
        self.Sessions = ["", "", "", ""]

    def Lecture_sign_in(self, day):
        """Sign-in function for a lecture on a given day of the workshop.  This
        will throw an exception if called more than once for a given day.

        Keyword arguments:
        day -- The day of the workshop (ordinal, not date.)
        """
        if not self.Lectures[day]:
            self.Lectures[day] = True
        else:
            raise DoubleWriteException(self.EmailAddress, day)

    def Session_sign_in(self, day, session):
        """Sign-in function for afternoon sessions on a given day of the
        workshop. If more than one login is attempted on a particular day, this
        throws an exception.

        Keyword arguments:
        day     -- The day of the workshop (ordinal, not date.)
        session -- The name of the session attended.
        """
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
