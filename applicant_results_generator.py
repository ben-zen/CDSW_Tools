"""Applicant Results Generator, a basic TSV to CDSW session file converter.

The basic format of the file is an email address in the first column, and either
Yes or No with a newline immediately after it in the second column.  (Yes
correlates to Accepted, No correlates to waitlisted.)
"""
# Copyright (C) 2015 Ben Lewis
# Licensed under the MIT license
# Tool for generating useful sets of accepted/declined CDSW applicants, and then
# exporting them to a file for later use.

import argparse
import cdsw
import os
import pickle
import sys

parser = argparse.ArgumentParser()

parser.add_argument("SessionName",
                    help=("Name of the session you're generating this data for,"
                          " used for naming the output file."))
parser.add_argument("SourceFile",
                    help=("File name of the source TSV used for generating the"
                          " output sets."))

args = parser.parse_args()

# Create the name we'll print this data to right now
output_template = "CDSW_Applicant_Data_{0}.pydata"
output_name = output_template.format(args.SessionName.replace(" ", "_"))
print(output_name)


session_data = cdsw.Workshop()

# Before we actually open the source file, better to check that it's valid.
if not os.path.isfile(args.SourceFile):
    print("No file at {0}.".format(args.SourceFile))
    sys.exit(os.EX_IOERR)
elif not os.access(args.SourceFile, os.R_OK):
    print("Cannot read file at {0}.".format(args.SourceFile))
    sys.exit(os.EX_IOERR)

if os.path.exists(output_name):
    print("A file already exists at '{0}'.".format(output_name))
    sys.exit(os.EX_IOERR)

with open(args.SourceFile, "r") as applicants :
    for line in applicants:
        email,accepted_state = line.split("\t")
        email.strip()
        email = email.lower()
        if ("@" in email):
            if accepted_state == "Yes\n" : # The newline is from the TSV.
                session_data.Add_attendee(email)
            else:
                session_data.Add_to_waitlist(email)

out_file = open(output_name, 'wb')

pickle.dump(session_data, out_file)

out_file.close()

summary_statistics = {
    "Name" : args.SessionName,
    "AcceptedStudents" : len(session_data.Attendees),
    "WaitlistedStudents" : len(session_data.Waitlist)
}

summary_wording = """
Summary
-------
Session: %(Name)s
# of students accepted: %(AcceptedStudents)d
# of students waitlisted: %(WaitlistedStudents)d
"""

print(summary_wording % summary_statistics)
