#!/usr/bin/env python
""" Translating into Protein sequence
IN This program we are expecting to get protein sequence by using transcribe and translate functions
"""

#importing libraries
import argparse
import re
from Bio.Seq import Seq
from Bio import SeqIO



def get_args():
    """Return parsed command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Getting input directly from file using arg parse.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # get the FASTA file of sequences
    parser.add_argument('filename',  # variable to access this data later: args.filename
                        metavar='FASTA', # shorthand to represent the input value
                        help='Provide name and path to FASTA file to process.', # message to the user, it goes into the help menu
                        type=str)
    parser.add_argument('-p', '--pattern',  # access with args.pattern
                        help='Provide a regex pattern for filtering FASTA entries',
                        default='^\d{1}\D*$')  # default works for Drosophila chromosomes

    return(parser.parse_args())



def find_first_orf(rna):
    """Return first open-reading frame of RNA sequence as a Bio.Seq objec
    """
    try:
        #TODO update regex to find the ORF
        orf = re.search('AUG([AUGC]{3})+?(UAA|UAG|UGA)', str(rna)).group()
    except AttributeError:  # if no match found, orf should be empty
        orf = ""
    return(Seq(orf))


def translate_first_orf(dna):
    """Translating the dna sequences first then translating the rna to protein
    Assumes input sequences is a Bio.Seq object.
    """
    dna = Seq(dna)
    # by giving this command we are transcribing the dna to rna using function called transcribe()
    rna = dna.transcribe()
    ss_orf = find_first_orf(rna)
    # here we are translating the rna to protein using the function called translate()
    translated_orf = ss_orf.translate()
    # this command returns the protein sequence
    return(translated_orf)

if __name__ == "__main__":
    # getting argument through command line
    args = get_args()
    sequence_list = args.filename
    seq_pattern = args.pattern
    # parsing the handle to obtain the record
    for record in SeqIO.parse(sequence_list, "fasta"):
        if re.match(seq_pattern, record.id):
            # here this command gives output
            print(record.id,translate_first_orf(record.seq))