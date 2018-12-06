```bash
python3 main.py --help
```
## nlp setup
```bash
pip install -r requirements.txt
```

## nlp server start[Optional]
```bash
# 如果下载速度太慢的话，北航校园网下可以去"ftp://10.111.1.29/share-folder"里下载stanford-corenlp-full-2018-10-05.zip，那里传了一份
wget https://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip
解压后，cd到其文件夹内
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
```

## ToDoList
- [ ] 代码开发
- [ ] Demo结果
- [x] newest design of model
- [x] OCl  
--by shifaqiang