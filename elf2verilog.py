#!/usr/bin/python
import argparse
import subprocess
import sys
import os

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

def getArgs():
    argp = argparse.ArgumentParser()
#    argp.add_argument("saddr", default = 0, metavar = "s", type=int , help = "Starting Address")
    argp.add_argument("input", metavar = "f", type = str, help = "Input Hex File")
    argp.add_argument("--ram-name", default="ram", metavar = "r", type = str, help = "Name of RAM variable")
    argp.add_argument("--no-space", default=None, help = "Remove extra newline every 32 bits")
    argp.add_argument("--output", "-o", default="/dev/stdout", help="Output File")
    return argp.parse_args()

def generateAssemblerFile(cFile, output):
    gccCall = f"riscv32-unknown-elf-gcc -march=rv32id -S -o {output} {cFile}"
    res = subprocess.run(gccCall, shell=True, errors=True)
    if res.returncode != 0:
        raise Exception("GCC Failed")

def generateElfFile(asFile, output):
    asCall = f"riscv32-unknown-elf-as -o {output} {asFile}"
    res = subprocess.run(asCall, shell=True, errors=True)
    if res.returncode != 0:
        raise Exception("AS Failed")

def generateHexFile(elfFile, output):
    elf2hexCall = f"riscv32-unknown-elf-elf2hex --bit-width 32 --input {elfFile} --output {output} "
    res = subprocess.run(elf2hexCall, shell=True, errors=True)
    if res.returncode != 0:
        raise Exception("elf2hex Failed")
    
def main():
    args = getArgs()

    workDir = "/tmp/.elf2vrlg"
    os.makedirs(workDir, exist_ok=True)
    try: 
        generateAssemblerFile(args.input, workDir + "/a.s")
        generateElfFile(workDir + "/a.s", workDir + "/a.out")
        generateHexFile(workDir + "/a.out", workDir + "/a.hex")
    except Exception as e:
        sys.stderr.write(f"error: Exception during compilation: {e}")
        exit(1)
        
    inputAsm = getContents(workDir + "/a.hex")
    outputAsm = transformInput(inputAsm, startAddr=64,
                               ramName=args.ram_name, noSpace=args.no_space)
    writeOutput(outputAsm, args.output)

main()
            
