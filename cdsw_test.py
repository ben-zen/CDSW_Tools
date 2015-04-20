"""Unit tests for the CDSW module."""
# Copyright (C) 2015 Ben Lewis <benjf5+github@gmail.com>
# Licensed under the MIT license.

import unittest
import cdsw

class TestAttendee(unittest.TestCase):

    """Provides unit tests for the CDSW Attendee class.

    Tests for lecture sign-in and session sign-in success, as well as checks
    that multiple attempted sign-ins will be rejected appropriately.
    """

    def setUp(self):
        self.attendee = cdsw.Attendee("test@example.org")

    def test_signin(self):
        self.attendee.Lecture_sign_in(0)
        self.assertTrue(self.attendee.Lectures[0])

    def test_multiple_signin(self):
        self.attendee.Lecture_sign_in(0)
        with self.assertRaises(cdsw.DoubleWriteException):
            self.attendee.Lecture_sign_in(0)

class TestWorkshop(unittest.TestCase):

    def setUp(self):
        self.workshop = cdsw.Workshop()
        self.workshop.Add_attendee("attend@example.org")
        self.workshop.Add_to_waitlist("wait@example.org")

    def test_add_attendee(self):
        self.workshop.Add_attendee("add_test@example.org")
        self.assertTrue("add_test@example.org" in self.workshop.Attendees)

    def test_add_same_attendee(self):
        with self.assertRaises(cdsw.PreexistingAddressException):
            self.workshop.Add_attendee("attend@example.org")

    def test_add_to_waitlist(self):
        self.workshop.Add_to_waitlist("wait_test@example.org")
        self.assertTrue("wait_test@example.org" in self.workshop.Waitlist)

    def test_add_same_to_waitlist(self):
        with self.assertRaises(cdsw.PreexistingAddressException):
            self.workshop.Add_to_waitlist("wait@example.org")

    
if __name__ is "__main__":
    unittest.main()
