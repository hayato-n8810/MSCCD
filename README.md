## Summary
多言語対応コードクローン検出ツール MSCCD

https://github.com/zhuwq585/MSCCD よりフォーク


## Features

ICPC2022で採択された論文 https://arxiv.org/pdf/2204.01028.pdf 

## Docker Image

提供されているDockerイメージを使用することで，環境依存の設定を回避できます．

Link: https://drive.google.com/file/d/17zsCf-5FnKbE1iPw6Ca4onW5ckQX69eQ/view?usp=sharing 

MSCCD は /root/MSCCD にあります．

最新の MSCCD に更新するには **git pull** を実行してください．

./dockerImage直下にダウンロードしてください

```
docker compose -d
```
で動作します．


## Environment dependence

MSCCD は Ubuntu 18.04LTS / MacOS Monterey　でテスト済みです．

MSCCDは主に以下の環境に依存しています:
+ Python v3.6.9
+ Java 11 (Newer than Java9) (異なるバージョンを使用する場合，modules/msccd_tokenizers/pom.xmlを編集してバージョンを設定してください)
+ Maven v3.8.5
+ jinja2 (pip3)
+ ujson (pip3)

ANTLR4.8にいくつかのインターフェースとメソッドを追加し、MSCCD用の.jarファイルをパッケージ化しました．提供されたantlr-4.8-modified.jarをローカルのMavenリポジトリにインストールしてください．

    mvn install:install-file -Dfile=./lib/antlr-4.8-modified.jar -DgroupId=org.nagoya_u.ertl.sa -DartifactId=antlr-v4.8-modified -Dversion=4.8 -Dpackaging=jar 

## Generate a tokenizer for the target language

まず，./parserConfig.json を編集します：
+ parser: 言語ごとの文法規則フォルダーまでのパス（g4 ファイルと場合によっては Java プログラムを含む）**grammarDefinations/{言語名}**
+ grammarName: g4 ファイルで定義された言語名．grammarsv4 からの場合は pom.xml でも確認可能
+ startSymbol: pom.xmlのentryPoint または parser.g4 ファイルのoptionsの前後で確認可能

次に，トークナイザーを生成します:

    python3 tokenizerGeneration.py 


## Configure the tool

ツールは *config.json* で以下の項目を設定できます：

+ inputProject: 検出対象プロジェクトのパスのリスト
+ keywordsList: キーワードリストのパス（grammarDefinations/{言語名}/***.reserved）
+ languageExtensionName: 対象言語の拡張子
+ minTokens: クローン検出時のトークンバッグの最小サイズ
+ minTokensForBagGeneration: トークン化時のトークンバッグの最小サイズ．小さい値を設定すると，クローン検出時のトークンバッグのサイズ範囲が広くなる．大きい値を設定すると，小さなバッグを避けたい場合にトークナイザーの処理が高速化される
+ detectionThreshold: 類似性閾値（0から1の範囲の数値）．コードペアの重なり類似性が閾値を超える場合，それらをクローンと見なす．閾値を高くすると精度が向上し再現率が低下し，逆もまた然り．
+ maxRound: 検出する最大粒度値
+ tokenizer: 生成されたトークナイザーの名前（parserConfig.jsonの "grammarName" と同じ）
+ threadNum_tokenizer
+ threadNum_detection


## Execute MSCCD

同じプロジェクトで複数の検出を実行する必要がある場合のために，必要なデータをタスクオブジェクトに保存可能（次回実行時の時間節約）．

### Execute for the first time（設定ファイルから新しいタスクを生成してツールを実行する）

1 *config.json* ファイルを編集し，文法ファイル・キーワードリストファイル・入力ファイルを確認

2 controller.py を実行し結果を待つ

    python3 controller.py


3 *tasks/task[taskId]/*　を確認する．各実行ごとに，結果ファイルを保存するための *detection* という名前のフォルダーが作成される

### Execute from a generated task（生成されたタスクからツールを実行する）
コマンドで検出の粒度と閾値をオプションで簡単に変更可能

    python3 controller.py [taskId] ([statementThreshold])
 

例：
+ **python3 controller.py 1** はtasks/task1から実行 
+ **python3 controller.py 2 0.9** はtasks/task2から，検出閾値（detectionThreshold）を0.9に設定


## Check the detection results.

 各タスクのデータは、設定ファイル、ファイル一覧、トークンバッグを含むtasks/task*フォルダーに保存される:
 | file | description |
 | --- | --- |
 | fileList.txt | 各行はソースファイルを表し，(プロジェクトID, ファイルパス)の形式でフォーマットされている．各プロジェクト内の各ファイルのインデックスはfileIdとして定義される． |
 |tokenBags | 各行はトークンバッグを表し，各データフィールドは 『@ @』 で区切り：projectId @ @ fileId @ @ bagId @ @ granularity value @ @ number of keywords @ @ symbol number @@ token number @@ original fileの開始行 -- original fileの終了行@@ tokens(token text :: frequency)  |
 | taskData.obj | 設定 |

  各検出の結果は、tasks/task*/detection* フォルダーに保存される．
 | file | description |
 | --- | --- |
 | pairs.file | クローンを検出したファイルペア [[projectId,fileId,bagId],[projectId,fileId,bagId]] |
 | info.obj | 実行時間など |


## Scripts:

+ **scripts/blockPairOutput.py**：CSV形式の出力ファイルを生成
+ フォーマット： [file1Path,startLine,endLine,file2Path,startLine,endline]
+ 出力先： ./result/task*/detection*/blockPair.csv
```
python3 scripts/blockPairOutput.py taskId detectionId   
```
+ **scripts/filePairOutput.py** : CSV形式の出力ファイルを生成
+ MSCCDをファイルレベルクローン検出器として実行する場合に利用. (config.jsonで maxRound を1または0に設定した場合)
+ フォーマット： [file1Path,file2Path]
+ 出力先： ./result/task*/detection*/filePair.csv
```
python3 scripts/filePairOutput.py taskId detectionId
```

## Comming soon

+ Speed up 
+ Analysis scripts to make the detection results easier to read and use
