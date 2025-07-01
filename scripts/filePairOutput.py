## input: taskId, detectionId
## output: clone pair of file identifier
## parameters: taskId detectionId outputFile
import sys, os, ujson

MSCCD_ROOT = "./"
def cloneListGeneration(clonePath):
    res = []
    for cloneLine in open(clonePath, "r").readlines():
        res.append(ujson.loads(cloneLine[:-1]))
    
    return res
    
def fileListGeneration(fileListPath):
    res = []
    splitTmp = None
    for dataLine in open(fileListPath,"r").readlines():
        splitTmp = dataLine[:-1].split(",")
        projectId = int(splitTmp[0])
        while len(res) - 1 < projectId:
            res.append([])
        res[projectId].append(splitTmp[1])
    
    return res


if __name__ == "__main__":
    taskId = sys.argv[1]
    detectionId = sys.argv[2]
    outputFile = f"./result/task{taskId}/detection{detectionId}/filePair.csv"
    # taskId = "1"
    # detectionId = "1"
    # outputFile = 'output.txt'
    fileList  = MSCCD_ROOT + "tasks/task" + taskId + "/fileList.txt"
    cloneList = MSCCD_ROOT + "tasks/task" + taskId + "/detection" + detectionId + "/pairs.file"
    res = []
    
    if os.path.exists(fileList) and os.path.exists(cloneList):
        fileListArr  = fileListGeneration(fileList)
        cloneListArr = cloneListGeneration(cloneList)
        
        for clone in cloneListArr:
            res.append( (fileListArr[clone[0][0]][clone[0][1]], fileListArr[clone[1][0]][clone[1][1]]) )
        
        if not os.path.exists(outputFile):
            # ディレクトリ部分を抽出
            dir_path = os.path.dirname(outputFile)

            # ディレクトリが存在しない場合は作成
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            # 空ファイルを作成
            with open(outputFile, 'w') as f:
                pass

            print(f"{outputFile} を作成しました。")
        else:
            print(f"{outputFile} は既に存在します。")

        with open(outputFile,"w") as f:
            for filePair in res:
                f.write(filePair[0] + "," + filePair[1] + "\n")
    else:
        print("File not exist.")    


