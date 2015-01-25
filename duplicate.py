#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports
import sys
import argparse

# argparser
argparser = argparse.ArgumentParser(description='Duplicate code searcher')
argparser.add_argument('-i', help="input file")
argparser.add_argument('-o', help="output file")
argparser.add_argument('--no_spaces', action='store_true', help="don't compare spaces")
argparser.add_argument('-s', action='store_true', help="silent mode")
argparser.add_argument('-n', help="number of minimum consecutive lines")
args = argparser.parse_args()


def readFile():
    original = open(args.i,'r')
    lines = []
    for index, line in enumerate(original):
        # only take used lines in our array
        if line.strip():
            # make the search work over different indents
            x = line.strip()
            if args.s:
                # make the search disregard spaces
                x = x.replace(" ", "")
            lines.append({'lineNr':index+1, 'line':x, 'originalLine':line})
    return lines

def printBlock(block):
    printResult = "Duplicate found:\n"
    for line in block:
        first = line['first']
        next = line['next']
        printResult += ("%s/%s - %s" % (first['lineNr'], next['lineNr'], first['originalLine']))
    printResult += "\n"
    return printResult


if __name__=='__main__':

    lines = readFile()
    if not args.n:
        cons = 3
    else:
        cons = int(args.n)

    if not args.i:
        sys.exit("No file specified")

    if not args.o and args.s:
        sys.exit("Running the script in silent mode without output file is kinda stupid, no?")

    linesbak = list(lines)
    result = []
    iline = 0
    # iterate through the lines to see if we find a matching line
    while iline < len(lines):
        line = lines[iline]
        # we can pop the first item at the beginning, as it will be the same as the original anyway
        linesbak.pop(0)
        for icomp, comp in enumerate(linesbak):
            # first match
            # skip blank lines
            if comp['line'] == line['line']:
                block = [{'first':line, 'next':comp}]
                match = 1 # let's start counting the lines
                rest = list(linesbak[icomp:])
                rest.pop(0)
                # iterate through the next consecutive lines
                for item in rest:
                    if item['line'] == (lines[iline+match])['line']:
                        block.append({'first':lines[iline+match], 'next':item})
                        match += 1
                    else:
                        break
                if match >= cons:
                    result.append(block)
                    printBlock(block)
                    iline += match
                    [linesbak.pop(0) for _ in range(match)]
        iline +=1

    # output part
    output = ""
    for hit in result:
        output += printBlock(hit)

    if not args.s:
        if output.strip():
            print(output)
        else:
            print("No duplicates found")
    if args.o:
        try:
            f = open(args.o, 'w')
            f.write(output)
            f.close()
        except Exception as e:
            print("An error occured while writing the file: \n %s" %(e))
