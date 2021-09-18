from zipfile import ZipFile
import os
from os.path import basename
import re
import glob
import random

# The program zips all the files for every submission and then it divides those assignments among the graders
# You can download all files in the grade center

# Give the directory where the assignments are stored
dir = ''

graders = [
    'Jeroen',
    'Jurjen',
    'Andreaa',
    'Satchit',
    ]

# Zip the files from given directory that matches the filter
def zipFilesInDir(zipFileName, filter):
    # create a ZipFile object
    with ZipFile(dir + "/assignments_divided" + "/" + zipFileName, 'w') as zipObj:
        # Iterate over all the files in directory
        filenames = os.listdir(dir)
        for filename in filenames:
            if filter(filename):
                # create complete filepath of file in directory
                filePath = os.path.join(dir, filename)
                # Add file to zip
                zipObj.write(filePath, basename(filePath))

# Looks through all the files and finds every unique s number
def extract_unique_s_numbers(files):
    unique_s_numbers = []
    for file in files:
        # search for the s number in the file name
        s_number = re.search("(?<=_)(.*)(?=_attempt)", file)
        if s_number:
            if not s_number.group() in unique_s_numbers:
                unique_s_numbers.append(s_number.group())

    return unique_s_numbers

# Not entirely sure how this works, could use some documentation
def divide_assignments():
    #
    target_folder = dir + "/assignments_divided"
    ALLOWED_FILETYPES = ['zip']

    filenames = []
    for filetype in 'zip':
        filenames.extend(glob.glob("%s/*.%s" % (target_folder, filetype)))
    num_files = len(filenames)
    num_graders = len(graders)
    files_per_grader = num_files // num_graders
    random.shuffle(filenames)
    # print(filenames)

    print("Creating a random division of %d files over %d graders (%d per grader, %d remainder)" % (
    num_files, num_graders, files_per_grader, num_files % num_graders))

    part_start = 0
    for grader in graders:
        to_move = filenames[part_start:part_start + files_per_grader]
        print('\n'.join(to_move))
        os.makedirs(target_folder + '/' + grader, exist_ok=True)
        for file in to_move:
            file_trunc = file[len(target_folder) + 1:]
            os.rename(target_folder + '/' + file_trunc, target_folder + '/' + grader + '/' + file_trunc)
        print('====')
        part_start += files_per_grader

    # deal with remainder
    print(filenames[part_start:])

def main():
    # Get the names of all the files and directories in dir
    files = os.listdir(dir)

    # Get every unique s_number that is in the file names
    unique_s_numbers = extract_unique_s_numbers(files)

    # Create a folder assignments divided if it is not there already
    if not os.path.exists(dir + "/assignments_divided"):
        os.makedirs(dir + "/assignments_divided")

    # Create a zip file for every unique s number. The functions looks for all the files that are
    # from a certain student and puts it in a zip file. This is done for every submission
    for unique_s_number in unique_s_numbers:
        zipFilesInDir(unique_s_number + '.zip', lambda name: unique_s_number in name)

    # Divide the assignments among the graders
    divide_assignments()


if __name__ == '__main__':
   main()