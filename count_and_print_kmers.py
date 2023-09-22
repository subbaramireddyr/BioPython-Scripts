#!/usr/bin/env python
"""Count and print k-mers

Given a user-provided sequence and optional k-mer length (default = 6)
"""

import argparse


def get_args():
    """Return parsed command-line arguments."""

    parser = argparse.ArgumentParser(
        description='Count and Print K-mers',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('sequence',
                        help='Input a sequence to break into k-mers',
                        type=str)

    parser.add_argument('-k', '--kmer_length',
                        metavar='INT',
                        help='Size of k-mers to break the sequence into',
                        type=int,
                        default=6)

    return(parser.parse_args())


def count_kmers(sequence, kmer_length):
    """Return sequence and count of k-mers of length kmer_length"""

    # Initialize a k-mer dictionary
    kmer_dictionary = {}
    stop = len(sequence) - kmer_length + 1

    # Iterate over the positions
    for start in range(0, stop):
        # Get the substring at a specific start and end position
        kmer = sequence[start:start + kmer_length]

        # Increase the count of this kmer by 1
        # if the kmer is new, start at 0 before incrementing by 1
        kmer_dictionary[kmer] = kmer_dictionary.get(kmer, 0) + 1

    return(kmer_dictionary)


if __name__ == "__main__":
    args = get_args()
    kmer_count = count_kmers(args.sequence, args.kmer_length)

    # Iterate over the k-mers and counts in the dictionary
    for kmer, count in kmer_count.items():
        print(f'{kmer}\t{count}')
