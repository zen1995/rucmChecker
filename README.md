```bash
python3 main.py --help
```
## nlp setup
```bash
pip install -r requirements.txt
# 如果下载速度太慢的话，北航校园网下可以去"ftp://10.111.1.29/share-folder"里下载stanford-corenlp-full-2018-10-05.zip，那里传了一份
wget https://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip
解压到本目录下
python start_nlp_server.py

# 测试nlputil是否正常工作
python nlputils.py
```