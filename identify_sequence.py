#!/usr/bin/env python
""" finding identity_sequence
code checks whether the sequence is nucleic acid and amino acid and not amino or nucleic acid using manual and automated testing using pytest
"""

import argparse


def get_args():
    """Return parsed command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Checks and recognise as amino acid or nucleic acid",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # get a list of text files to process
    parser.add_argument('file_list',  # variable to access this data later: args.file_list
                        metavar='FILE', # shorthand to represent the input value
                        help='Provide file name to process. For multiple files, separate their names with spaces.', # message to the user, it goes into the help menu
                        type=str,
                        nargs="+" # will combine multiple textfile inputs into a list
                        )

    return(parser.parse_args())


def identify_sequence(sequence):
    # this is the path to open sequence3 file.
    sequence_path = sequence
    # this command allows each line to read in upper case
    seq_lines = sequence_path.upper()
    # here we created a string and labelled as nucleotides
    nucleotides = ['A', 'T', 'G', 'C', 'U']
    amino_acids = ['Q','W', 'E', 'R', 'T', 'Y', 'I', 'P', ' A', 'D', 'F', 'G', 'H','K', 'L', 'C', 'V', 'N', 'M', 'S']
    check_file = True
    # here every line is iterated
    for line in seq_lines:
        # here every letter is iterated
        for letter in line:
            if letter in amino_acids and letter not in nucleotides:
                check_file = False
            elif letter not in nucleotides:
                return 'not amino acid or nucleic acid'
    if check_file is True:
        sequence_type = 'nucleic acid'
    else:
        sequence_type = 'amino acid'

    return sequence_type

if __name__ == "__main__":
    args = get_args()
    # TODO: loop through args.file_list to:
    for sequence_file in args.file_list:
        with open(sequence_file,'r') as NA_AA_file:
            sequence = NA_AA_file.readline()
            sequence = ''.join(sequence)
            print(identify_sequence(sequence))


