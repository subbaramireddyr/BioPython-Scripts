#!/usr/bin/env python3
"""This programs helps in combining(interleaving) input files(two files) into one output file """

# parsing command-line argument
import argparse
# this module to get current timestamp
from datetime import datetime
# this module reading or writing FASTQ/A files
from Bio import SeqIO


def get_args():
    """ parsing command-line arguments are returned ."""
    parser = argparse.ArgumentParser(
             description="Interleave mate-pair FASTQ sequences into a single FASTA file.",
             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # variable to access this data later: args.output
    parser.add_argument('-mate1', '--sequence1',
                        # shorthand to represent the input value
                        metavar='FASTQ',
                        help='Provide the path for the output FASTA file.',
                        # message to the user, it goes into the help menu
                        type=str,
                        required=True)
    # variable to access this data later: args.output
    parser.add_argument('-mate2', '--sequence2',
                        metavar='FASTQ',  # shorthand to represent the input value
                        help='Provide the path for the output FASTA file.',
                        # message to the user, it goes into the help menu
                        type=str,
                        required=True)

    # this command is used to get output FASTA file name
    parser.add_argument('-o', '--output',  # variable to access this data later: args.output
                        metavar='FASTA', # shorthand to represent the input value
                        help='Provide the path for the output FASTA file.', # message to the user, it goes into the help menu
                        type=str,
                        required=True)

    # this command is used to extra arguments to help us format our log file output
    parser.add_argument('--logFolder',  # variable to access this data later: args.logFolder
                        # message to the user, it goes into the help menu
                        help='Provide the folder for log files.',
                        type=str,
                        default="results/logs/")
    # variable to access this data later: args.logBase
    parser.add_argument('--logBase',
                        help='Provide the base for the log file name',
                        type=str,
                        default=parser.prog)  # get the name of the script

    return(parser.parse_args())


def pathLogFile(logFolder, logBase):
    """Return a log file path and name using the current time and script name."""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")  # get current time in YYYY-MM-DD-HHMM
    return(f"{logFolder}{timestamp}_{logBase}.log")


def interleave(mate1, mate2):
    """Return list of interleaved SeqRecords.
    Assumes mate1 and mate2 inputs are SeqIO.parse iterator objects.
    """
    # initialize an empty list
    interleaved = []
    # this command is used to populate the interleaved list with interleaved SeqRecord objects
    for l, r in zip(list(mate1), list(mate2)):
        interleaved.append(l)
        interleaved.append(r)
    return(interleaved)


def logInterleave(args):
    """Create log of Interleave progress."""
    logFile = pathLogFile(args.logFolder, args.logBase)
    # this command is used to open logfile in writing mode
    with open(logFile, 'w') as log:
        log.write(f"Running interleaved.py on {datetime.now()}\n")
        log.write("\n**** Summary of arguments ****")
        # this command is used to log the two mate files and the output file
        log.write(f"\nFirst Argument: {args.sequence1}")
        log.write(f"\nSecond Argument: {args.sequence2}")
        # we don't need to log our args.logFolder and args.logBase
        # this command is used add some space between argument data and the rest of the log
        log.write("\n\n")
        log.write(f"\nPreparing input data - {datetime.now()}")
        # this command is used load input from a file
        log.write(f"\nCalling heart() to process the data - {datetime.now()}")
        # this command is used to add code to output results as needed
        log.write(f"\nOutputing results to file - {datetime.now()}")
        # this command is used to get the FASTQ sequences with SeqIO.parse
        mate1 = SeqIO.parse(args.sequence1, "fastq")
        # this command is used to get the interleaved list of SeqRecord objects
        mate2 = SeqIO.parse(args.sequence2, "fastq")
        #  this command is used to write the
        #  interleaved list of SeqRecord objects to our FASTA file with SeqIO.write
        interleaved = interleave(mate1, mate2)
        SeqIO.write(interleaved, args.output, "fasta")
        log.write(f"\nScript has finished at {datetime.now()}")

if __name__ == "__main__":
    # pass arguments directly into the primary function
    logInterleave(get_args())
