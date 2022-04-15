import os
import shutil
import logging

# logger config
logger = logging.getLogger('MASTER')
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s][%(filename)s][%(levelname)s][%(lineno)d]: %(message)s', '%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

def getPath():
    srcPath = input(">>> Source Path:")
    dstPath = input(">>> Destination Path:")
    return (srcPath, dstPath)

def checkPath(srcPath, dstPath):
    res = True
    if not os.path.isdir(srcPath):
        res = False
        print('source path: \'' + srcPath + '\' is invalid.')
    if not os.path.isdir(dstPath):
        res = False
        print('destination path: \'' + dstPath + '\' is invalid.')
    return res

def moveFile(srcPath, dstPath, filenames):
    res = True
    for filename in filenames:
        if str(filename)[0].isdigit():
            # [0-9]
            dstDirPath = dstPath + '\\[0-9]'
        else:
            dstDirPath = dstPath + '\\[' + str(filename).upper()[0] + ']'
        if not os.path.exists(dstDirPath):
            os.makedirs(dstDirPath)
        if not os.path.exists(dstDirPath + '\\' + filename):
            print('moving ' + str(filename) + ' ...')
            shutil.move(srcPath + '\\' + filename, dstDirPath)
            print('\"' + str(filename) + '\" is moved successfully.')
        else:
            print('Filename: ' + str(filename) + ' is existed.')
            res = False
    return res

def deleteFile(srcPath, filenames):
    if os.path.exists(srcPath):
        if filenames == None:
            print('removing ' + str(srcPath) + ' ...')
            shutil.rmtree(srcPath)
            print('\"' + str(srcPath) + '\" is deleted successfully.')

if __name__ == "__main__":

    # input source and destination path
    (srcPath, dstPath) = getPath()
    if not checkPath(srcPath, dstPath):
        print('Please check whether source and destination path are valid.')
        exit

    # get path of all files
    FileList = []
    for root, dirs, files in os.walk(srcPath):
        for file in files:
            if str(file).lower().endswith(tuple(['.avi', '.mp4'])):
                Temp = None
                for item in FileList:
                    if item[0] == root:
                        Temp = item
                        break
                if Temp == None:
                    FileList.append([root, file])
                else:
                    Temp.append(file)

    # process FileList
    for item in FileList:
        # move file from src to dst
        res = moveFile(item[0], dstPath, item[1:])

        # delete src folder if success
        if res:
            if item[0] == srcPath:
                deleteFile(item[0], item[1:])
            else:
                deleteFile(item[0], None)