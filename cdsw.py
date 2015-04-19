"""Provides useful classes for logging information about a CDSW session.

The session itself is managed through the Workshop class; an instance of that
object can be used to create new attendees and insert them into its
dictionary. The Workshop class can also generate metrics about attendees to
gauge continued involvement and interest.
"""
# Copyright (C) 2015 Ben Lewis
# Licensed under the MIT license.

from enum import Enum

class DoubleWriteException(Exception):

    """Thrown by a second attempt to write to a given field.

    Each element in an Attendee's Lectures and Sessions lists can only be
    written to once, and the only writes are setting a location in the Lectures
    array to True or a Sessions value to something other than the empty string.
    On an attempted second write, this exception is thrown.

    Members:
    EmailAddress -- Identifier of the throwing Attendee
    Day          -- Day of the workshop which the duplicate write was attempting
    Session      -- Optional argument.  If this is not `None`, the session field
                    for that day was being written to.  If it is `None`, then a
                    second checkin was attempted.
    """

    def __init__(self, email, day, session = None):
        super().__init__()
        self.EmailAddress = email
        self.Day = day
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
        """Sign-in function for a lecture on a given day of the workshop.

        Each attendee can sign in at most once for that mornings' lecture;
        any further attempt to sign in will throw a DoubleWriteException.

        Keyword arguments:
        day -- The day of the workshop (ordinal, not date.)
        """
        if not self.Lectures[day]:
            self.Lectures[day] = True
        else:
            raise DoubleWriteException(self.EmailAddress, day)

    def Session_sign_in(self, day, session):
        """Sign-in method for afternoon Workshop sessions.

        Each day of the workshop, an attendee can sign in to at most one
        session.  Any further attempt to sign in to a session will throw a
        DoubleWriteException.

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
        super().__init__()
        self.EmailAddress = email

class PreexistingAttendeeException(Exception):

    """Represents attempting to create an attendee that already exists."""

    def __init__(self, email):
        super().__init__()
        self.EmailAddress = email

class MissingAddressException(Exception):

    """Used when an address is not found in the waitlist."""

    def __init__(self, email):
        super().__init__()
        self.EmailAddress = email

class PreexistingAddressException(Exception):

    """Used when an address is already found on the waitlist."""

    def __init__(self, email):
        super().__init__()
        self.EmailAddress = email

class ApplicantStatus(Enum):

    """Enumeration of Workshop applicant states."""

    Accepted = 1
    Waitlisted = 2

class Workshop:

    """Stores all attendees and generates metrics for a CDSW session.

    Maintains a dictionary of Attendee objects with email addresses as keys, and
    provides methods to provide metrics on the Attendees.

    Members:
    Attendees -- Dictionary of attendees, using email addresses as primary keys.
    Waitlist  -- Set of waitlisted applicants; an applicant can be promoted to
                 Attendee status.
    """

    def __init__(self):
        self.Attendees = {}
        self.Waitlist = set()

    def Find_attendee(self, email):
        """Searches for an attendee in the dictionary.

        On failure, this method raises an MissingAttendeeException.

        Keyword arguments:
        email -- Email address for lookup in the dictionary.
        """
        if email in self.Attendees:
            return self.Attendees[email]
        else:
            raise MissingAttendeeException(email)

    def Add_attendee(self, email):
        """Add an attendee to the workshop, using their email address as key.

        If the email address is already present in the dictionary, this method
        raises a PreexistingAttendeeException.

        Keyword arguments:
        email -- Email address for lookup and Attendee creation.
        """
        if email not in self.Attendees:
            self.Attendees[email] = Attendee(email)
        else:
            raise PreexistingAttendeeException(email)

    def Add_to_waitlist(self, email):
        """Add an applicant to the waitlist for this Workshop session.

        Checks the waitlist first to make sure that the applicant is not already
        on the waitlist; if they are, raises a PreexistingAddressException.

        Keyword arguments:
        email -- Email address for the waitlist.
        """
        if email not in self.Waitlist:
            self.Waitlist.add(email)
        else:
            raise PreexistingAddressException(email)

    def Promote_from_waitlist(self, email):
        """Move an applicant from the waitlist to the attendee list.

        This method first checks that the provided address is in the waitlist,
        then removes it from the waitlist and adds an Attendee for that object
        to Attendees.  If the address is not found in the waitlist, this method
        raises a MissingAddressException.

        Keyword arguments:
        email -- Email address for lookup and Attendee creation.
        """
        if email in self.Waitlist:
            self.Waitlist.remove(email)
            self.Add_attendee(email)
        else:
            raise MissingAddressException(email)

    def Get_applicant_status(self, email):
        """Check if an applicant is accepted or waitlisted.

        This method first checks the attendee list, then checks the waitlist.
        If the supplied email address is not found, raises a
        MissingAddressException.

        Keyword arguments:
        email -- Email address for lookup.
        """
        status = None
        if email in self.Attendees:
            status = ApplicantStatus.Accepted
        elif email in self.Waitlist:
            status = ApplicantStatus.Waitlisted
        else:
            raise MissingAddressException(email)
        return status

    def Show_attendance_by_session(self, day):
        """Compute how many attendees signed in to each session on a day.

        For every attendee that signs in to one of the offered sessions, this
        method increments the counter for that session (or initializes it to one
        for a session that hasn't been encountered yet.

        Keyword arguments:
        day -- the day of the workshop for generating metrics (ordinal, not
               date.)
        """
        sessions = {}
        for x in self.Attendees.values():
            if (x.Sessions[day] in sessions) and (x.Sessions[day] is not ""):
                sessions[x.Sessions[day]] = sessions[x.Sessions[day]] + 1
            else:
                sessions[x.Sessions[day]] = 1
        return sessions
