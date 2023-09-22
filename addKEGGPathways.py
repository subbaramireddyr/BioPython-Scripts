#!/usr/bin/env python

"""
program: addKEGGPathways.py file

retrieving KEGG API online data for Genes, Orthologs, and Pathways connected with Uniprot IDs
and add to the file

"""

# importing requried libraries

import argparse
import requests


def get_args():
    """Return parsed command-line arguments."""

    parser = argparse.ArgumentParser(
        description="addKEGGPathways.py program to add KEGG Pathways to an output file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Create a sequential argument (eg. it has to come in the order defined)
    parser.add_argument('-i','--infile', '---infilename', # name of the argument, we will later use args.infile to get this user input
                        metavar='filename', # shorthand to represent the input value
                        help='filename', # message to the user, it goes into the help menu
                        type=str, # type of input expected, could also be int or float
                        default='./data/alignPredicted_1.txt', # default option if no input is given by the user
                        #required=False # whether this input must be given by the user, could also be True
                        )
    parser.add_argument('-e','--evalue', # name of the argument, we will later use args.evalue to get this user input
                        metavar='evalue', # shorthand to represent the input value
                        help='e value', # message to the user, it goes into the help menu
                        type=str, # type of input expected, could also be int or float
                        default='1e-50', # default option if no input is given by the user
                        #required=False # whether this input must be given by the user, could also be True
                        )

    # Create a flagged argument (eg. input comes after a short "-i" or long "--input" form flag)
    parser.add_argument('-o','--outfile', # name of the argument, we will later use args.outfile to get this user input
                        metavar='outfile', # shorthand to represent the input value
                        help='outfile', # message to the user, it goes into the help menu
                        type=str, # type of input expected, could also be int or float
                        default="./results/alignPredicted_1_results.txt", # default option if no input is given by the user
                        #required=False # whether this input must be given by the user, could also be True
                        )

    return(parser.parse_args())


def name_of_function(word, n=1):
    """
    This function does Return with duplicated words.
    """
    # it does things with the parameters above
    duplicated_word = word * n
    # returns the difined value
    return(duplicated_word)


def getUniProtFromBlast(blast_line, threshold):
    """
    If the evalue is less than the threshold, returns the UniProt ID from the BLAST line.
    If evalue is greater than the threshold, this function returns False.
    """
    cleaned_line = blast_line.strip()
    blast_fields = cleaned_line.split("\t")
    if float(blast_fields[7]) < float(threshold):
        return(blast_fields[1])
    else:
        return(False)


def loadKeggPathways():
    """
    From http://rest.kegg.jp/list/pathway/ko, return a dictionary wit h key=pathID and
    value=pathway name.
    """
    keggPathways = {}
    result = requests.get('https://rest.kegg.jp/list/pathway/ko')
    # for loop is used to loop over the each line
    for each_entry in result.iter_lines():
        if each_entry.decode(result.encoding):
            # this command help in conversion of binary value to plain text
            str_entry = each_entry.decode(result.encoding)
            # this command helps in split with the space
            fields = str_entry.split("\t")
            keggPathways[fields[0]] = fields[1]
    return(keggPathways)


def getKeggGenes(uniprotID):
    """
    Return a list of KEGG organism:gene pairs for a provided UniProtID.
    """
    keggGenes = []
    result = requests.get(f'https://rest.kegg.jp/conv/genes/uniprot:{uniprotID}')
    for each_entry in result.iter_lines():
        if each_entry.decode(result.encoding):
            # this command help in conversion of binary value to plain text
            str_entry = each_entry.decode(result.encoding)
            fields = str_entry.split("\t")
            keggGenes.append(fields[1])
    return(keggGenes)


def getKeggOrthology(keggGenes):
    """
    returns the ID for KEGG Orthology for a certain KEGG ID,

    based on the getKeggGenes() function.
    """
    kegg_Or = []
    kegg_Or_result = requests.get(f'https://rest.kegg.jp/link/ko/{keggGenes}')
    for each_entry in kegg_Or_result.iter_lines():
        if each_entry.decode(kegg_Or_result.encoding):
            str_entry = each_entry.decode(kegg_Or_result.encoding)
            fields = str_entry.split("\t")
            # print(fields[1])
            kegg_Or.append(fields[1])
    return(kegg_Or)


def getKeggPathIDs(keggOrthology):
    """
    returns the KEGG Path IDs for a KEGG Orthology ID, modeled after getKeggGenes ()
    function

    """

    kegg_p_ids = []
    result = requests.get(f'https://rest.kegg.jp/link/pathway/{keggOrthology}')
    for entry in result.iter_lines():
        if entry.decode(result.encoding):
            # print("decoded name is", entry.decode(result.encoding))
            str_entry = entry.decode(result.encoding)
            fields = str_entry.split("\t")
            kegg_p_ids.append(fields[1])
    return(kegg_p_ids)


def addKEGGPathways(blastFile, evalue, outputFile):
    """
    here this function checks for evalue and retrives the Uniprot id
    and KEGG Pathway IDs excluding map pathways gives the output file
    """
    kegg_p = loadKeggPathways()
    kegg_p_ids_1 = []
    outputFile = open(outputFile, "w")
    with open(blastFile, 'r') as nu_p_seq_file:
        for line in nu_p_seq_file:
            line = line.strip()
            # Check if the evalue is below the threshold and retrieve the UniProt ID
            up_ID = getUniProtFromBlast(line, evalue)
            if up_ID:
                # get the KEGG gene IDs
                kegg_Genes = getKeggGenes(up_ID)
                if kegg_Genes:
                    kegg_Or = getKeggOrthology(kegg_Genes[0])
                    # get the KEGG Pathway IDs
                    if kegg_Or:
                        kegg_p_ids = getKeggPathIDs(kegg_Or[0])
                        #print("path is", keggPathIDs)
                        for id in kegg_p_ids:
                            if not id.startswith("path:map"):
                                kegg_p_ids_1.append(id)
                                # print("yes")
                        if kegg_p_ids_1:
                            # Write the KEGG Pathway IDs excluding map pathways to the output file
                            for pathID in kegg_p_ids_1:
                                #print("in this loop", pathID)
                                f_line = line+"\t"+kegg_Or[0]+"\t"+pathID+"\t"+kegg_p[pathID]+"\n"
                                outputFile.write(f_line)

    nu_p_seq_file.close()
    outputFile.close()

if __name__ == "__main__":
    args = get_args()
    nu_p_File = args.infile
    evalue = args.evalue
    outputFile = args.outfile
    addKEGGPathways(nu_p_File, evalue, outputFile)