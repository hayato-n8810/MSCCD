import csv, sys

def filter_keyword_pair(csv_path, output_path, keyword):
    """ファイルパスを持つcsvから指定したキーワードを含むものを抽出

    Args:
        csv_path (str): csvのパス
        output_path (str): 出力ファイルのパス
        keyword (str): 抽出したいファイルのパスに含まれるキーワード
    """
    with open(csv_path, newline='', encoding='utf-8') as f_in, \
         open(output_path, 'w', encoding='utf-8') as f_out:
        reader = csv.reader(f_in)
        for row in reader:
            if any(keyword in item for item in row):
                f_out.write(','.join(row) + '\n')

if len(sys.argv) < 3:
    print("arguments are not enough")

else:
    # タスクIDと検出IDを入力から取得
    taskId = sys.argv[1]
    detectionId = sys.argv[2]

    # 実行
    filter_keyword_pair(f'./result/task{taskId}/detection{detectionId}/blockPair.csv', f'./result/task{taskId}/detection{detectionId}/blockPair_jsPerf.txt', "jsPerf")
