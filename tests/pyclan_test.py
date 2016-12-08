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
    #file = open('./output', 'w+')

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

def isHeaderAccurate(fline, sline):
    if (((fline.find("@") != -1) & (sline == "is_header --- True")) | ((fline.find("@") == -1) & (sline == "is_header --- False"))):
        return 0

    return "ERROR"

def isTierLineAccurate(fline, sline):
    if (((fline.find("*") != -1) & (sline == "is_tier_line --- True")) | ((fline.find("@") == -1) & (sline == "is_tier_line --- False"))):
        return 0

    return "ERROR"

def isTotalTimeAccurate(begin, end, time):

    if (begin == "time_offset --- None" & end == "time_onset --- None" & time == 0):
        return 0

    offset = int(filter(str.isdigit, begin))
    onset = int(filter(str.isdigit, end))
    total = int(filter(str.isdigit, time))

    if (offset - onset == total):
        return 0

    return "ERROR"

def isHeaderAndTierLine(fline, sline):
    if (((fline == "is_header --- True") & (sline == "is_header --- False")) | ((fline == "is_header --- False") & (sline == "is_header --- True"))):
        return 0

    return "ERROR"

def isTierLineAndisNotTier(fline, sline):
    if (((fline == "is_tier_line --- True") & (sline == "tier --- None")) | ((fline == "is_tier_line --- False") & (sline != "tier --- None"))):
        return 0

    return "ERROR"

for filename in glob.iglob('./Test Outputs/*.txt'):
     fname = open(filename, 'r')
     lines = fname.readlines()
     fileSize = len(lines)

     listOfIsHeaders = []
     listOfIsTiers = []
     listOfLineSymbols = []


     #verFile = open('./Output Verification/' + filename[15:20] + "_Verification" + ".txt", 'w+')
     for x in range(7, fileSize, 25):
         print lines[57]
         listOfIsHeaders.append(lines[x])
     for x in range(10, fileSize, 25):
         listOfIsTiers.append(lines[x])
     for x in range(13, fileSize, 25):
         listOfLineSymbols.append(lines[x])

     #for y in range(0, len(listOfIsHeaders), 1):

         #verFile.write(isHeaderAccurate(listOfLineSymbols[y], listOfIsHeaders[0]) + "\n")



