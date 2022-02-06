#!/usr/bin/python
import argparse
#import sys

def getContents(inputFileStr):
    inputCommands = list()
    with open(inputFileStr, "r") as inputFile:
        currentInput = "n"
        while currentInput:
            currentInput = inputFile.readline().strip("\n")
            if currentInput:
                inputCommands.append(currentInput)
    return inputCommands

def transformInput(inputAsm, startAddr, ramName, noSpace):
    outputAsm = list()
    for line in inputAsm:
        for i in range(0, 8, 2):
            bits = line[i:i+2]
            op = f"{ramName}[{startAddr}] <= 8'h{bits};"
            outputAsm.append(op)
            startAddr += 1
        if not noSpace:
            outputAsm.append("")

    return outputAsm

def writeOutput(output, outputFileStr):
    outputFile = open(outputFileStr, "a")
    for line in output:
        outputFile.write(line + "\n")
        
def main():
    argp = argparse.ArgumentParser()
    argp.add_argument("saddr", default = 0, metavar = "s", type=int , help = "Starting Address")
    argp.add_argument("input", metavar = "f", type = str, help = "Input Hex File")
    argp.add_argument("--ram-name", default="ram", metavar = "r", type = str, help = "Name of RAM variable")
    argp.add_argument("--no-space", default=None, help = "Remove extra newline every 32 bits")
    argp.add_argument("--output", "-o", default="/dev/stdout", help="Output File")
    args = argp.parse_args()

    inputAsm = getContents(args.input)
    outputAsm = transformInput(inputAsm, startAddr=args.saddr,
                               ramName=args.ram_name, noSpace=args.no_space)
    writeOutput(outputAsm, args.output)

main()
            
