import io
import subprocess

disassemble = "objdump -d --source -M intel "
directories = "find /usr/bin /bin /sbin -type f -executable -exec file -i '{}' \; | grep 'x-executable; charset=binary'"
numDirectories = subprocess.Popen(directories, shell=True, stdout=subprocess.PIPE)
dirResults = numDirectories.communicate()
dirList = []

for directory in dirResults:
    directoryStr = directory.decode()
    dirSplit = io.StringIO(directoryStr)
    for line in dirSplit:
        dirList.append(line.split(":")[0])
    break

print("Total Number of Linux Binaries: " + str(len(dirList)))
filesProcessed = 0;
dict = {}

for directory in dirList:
    filesProcessed += 1
    print("Total Files Currently Processed: " + str(filesProcessed))
    a = subprocess.Popen(disassemble + directory, shell=True, stdout=subprocess.PIPE)
    result = a.communicate()[0]
    resultStr = result.decode()
    s = io.StringIO(resultStr)
    for line in s:
        if (line != "\n" and len(line) >= 2 and line[2] == "4"):
            commandStr = (line.strip("\n"))[32:].split(" ")[0]
            if (commandStr):
                if (commandStr in dict.keys()):
                    dict.update({commandStr: dict.get(commandStr) + 1})
                else:
                    dict[commandStr] = 1;

print("\nOccurrences of Opcodes:")
for key, value in sorted(dict.items(), key=lambda item: item[1], reverse=True):
    print("%s: %s" % (key, value))
