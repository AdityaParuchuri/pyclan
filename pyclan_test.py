import sys
import glob
import os
from pyclan import *



if __name__ == "__main__":


    filepath = sys.argv[1]
    # print filepath

    folderPath = "/Volumes/Lexar/clan_files/"
    filePathToChaFiles = "/Volumes/Lexar/clan_files/*.cha"

    if (os.path.exists(folderPath)):
        print "Folder successfully found!"
    else:
        print "Failed to find folder :("

    if (os.path.exists(filepath)):
        print "File successfully found!"
    else:
        print "Failed to find file :("


    clan_file = ClanFile(filepath)
    # file = open('./output', 'w+')

    clanVar = ['content',
                'conv_block_num',
                'index',
                'is_clan_comment',
                'is_conv_block_delimiter',
                'is_end_header',
                'is_header',
                'is_multi_parent',
                'is_paus_block_delimiter',
                'is_tier_line',
                'is_tier_without_timestamp',
                'is_user_comment',
                'line',
                'multi_line_parent',
                'tier',
                'time_offset',
                'time_onset',
                'total_time',
                'within_conv_block',
                'within_paus_block',
                'xdb_average',
                'xdb_line',
                'xdb_peak']

    i = 1

# Uncomment below code to print .CHA output to file
'''
    for file in glob.glob(filePathToChaFiles):
        fname = file[26:31]
        file = open('./Test Outputs/' + fname + "output" + ".txt", 'w+')
        for line in clan_file.line_map:
            file.write("Line " + str(i) + " output: \n")
            i = i + 1
            for var in clanVar:
                #file.write(str(line.__dict__[var]) + "\n")
                file.write("{} --- {}\n".format(var, line.__dict__[var]))
'''



# testing filecount accuracy

lc = 25

def isHeader(fline, sline):
    if ((fline.find("@") != -1) & (sline.find("is_header --- True") != -1)):
        return 0

    return 1

def isTierLine(fline, sline):
    if ((fline.find("*") != -1) & (sline.find("is_tier_line --- True") != -1)):
        return 0

    return 1

def isUserComment(fline, sline):
    if ((fline.find("%xcom") != -1) & (sline.find("is_user_comment --- True") != -1) & (fline.find("|") == -1)):
        return 0

    return 1

def isGenComment(fline, sline):
    if ((fline.find("%com") != -1) & (sline.find("is_user_comment --- False") != -1) & (fline.find("|") != -1)):
        return 0

    return 1

def isTotalTimeAccurate(begin, end, time):

    if ((begin.find("time_offset --- None") != -1) & (end.find("time_onset --- None") != -1) & (time.find("total_time --- 0") != -1)):
        return 0

    offset = long(begin.split()[2])
    onset = long(end.split()[2])
    total = long(time.split()[2])

    if (offset - onset == total):
            return 0

    return 1


def isTierLineAndisNotTier(fline, sline):

    if (((fline.find("is_tier_line --- True") != -1) & (sline.find("tier --- None")) == -1) | ((fline.find("is_tier_line --- False") != -1) & (sline.find("tier --- None") != -1))):
        return 0

    return 1

for filename in glob.iglob('./Test Outputs/*.txt'):
     fname = open(filename, 'r')
     lines = fname.readlines()
     fileSize = len(lines)

     print fname

     listOfIsHeaders = []
     listOfIsTiers = []
     listOfIsUserComments = []
     listOfLineSymbols = []
     tiers = []
     totalTimes = []
     timeOffsets = []
     timeOnsets = []

     #############################################################################################
     #Uncomment below to create new folder with verification files
     verFile = open('./Output Verification/' + filename[15:20] + "_Verification" + ".txt", 'w+')
     #############################################################################################

     for x in range(0, fileSize, 1):
         headerID = lines[x][:9]
         if (headerID == "is_header"):
             listOfIsHeaders.append(lines[x])

         isTierID = lines[x][:12]
         if (isTierID == "is_tier_line"):
             listOfIsTiers.append(lines[x])

         commentID = lines[x][:15]
         if (commentID == ("is_user_comment")):
             listOfIsUserComments.append(lines[x])

         lineSymbolID = lines[x][:8]
         if (lineSymbolID == "line ---"):
             listOfLineSymbols.append(lines[x])

         tierID = lines[x][:8]
         if (tierID == "tier ---"):
             tiers.append(lines[x])

         totalTimeID = lines[x][:10]
         if (totalTimeID == "total_time"):
             totalTimes.append(lines[x])

         timeOffsetID = lines[x][:11]
         if (timeOffsetID == "time_offset"):
             timeOffsets.append(lines[x])

         timeOnsetID = lines[x][:10]
         if (timeOnsetID == "time_onset"):
             timeOnsets.append(lines[x])

     allVars = [listOfIsHeaders, listOfIsTiers, listOfLineSymbols, totalTimes, timeOffsets, timeOnsets, listOfIsUserComments, tiers]
     n = len(listOfIsHeaders)
     if all(len(x) == n for x in allVars):
        successfulOrNot = True
        print "Success! All variables are available"

     else:
        successfulOrNot = False
        print "Something is wrong; a variable is missing, or there is an extra variable\n"
        continue

     for y in range(0, len(listOfIsHeaders), 1):

         h = isHeader(listOfLineSymbols[y], listOfIsHeaders[y])
         t = isTierLine(listOfLineSymbols[y], listOfIsTiers[y])
         uc = isUserComment(listOfLineSymbols[y], listOfIsUserComments[y])
         gc = isGenComment(listOfLineSymbols[y], listOfIsUserComments[y])

         verFile.write("Index: " + str(y) + "\n")

         if (h == 0):
             verFile.write("Valid header.\n")
         elif (t == 0):
             verFile.write("Valid tier line.\n")
         elif (uc == 0):
             verFile.write("Valid user comment.\n")
         elif (gc == 0):
             verFile.write("Valid computer generated comment.\n")
         else:
             verFile.write("Invalid line.\n")

         if (isTierLineAndisNotTier(listOfIsTiers[y], tiers[y]) == 0):
             verFile.write("Valid tier line matching.\n")

         else:
             verFile.write("Invalid tier line.\n")

         if (isTotalTimeAccurate(timeOffsets[y], timeOnsets[y], totalTimes[y]) == 0):
             verFile.write("Total time is good!\n")
         else:
             verFile.write("Something is wrong with the time.\n")


