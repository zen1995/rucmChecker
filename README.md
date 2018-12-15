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

# 同理可到ftp://10.111.1.29/share-folder 上下载
wget https://nlp.stanford.edu/software/stanford-chinese-corenlp-2018-10-05-models.jar
# 启动中文server
java -Xmx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -serverProperties StanfordCoreNLP-chinese.properties -port 9001 -timeout 15000
```

## ToDoList
- [x] 代码开发
- [x] Demo结果
- [x] newest design of model
- [x] OCl  
--by shifaqiang
- [ ] 中文RUCM文件的分词与解释，请小帅哥杨森考虑能否实现，调查现有的中文分词工具
- [ ] 规则的再抽象与理解，实现规则的可扩展性，最帅的泽年继续设计呀
- [ ] 输出界面的美化，请审美小公主梁保宇考虑如何构造美丽的界面
- [ ] 运行过程全盘云端化，通过浏览器进行访问与展示，最丑陋的发强想办法
- [ ] 请子粤调研Python后端的web开发，尝试连接服务器与前端展示页面，主要沟通梁保宇
-- 2018年12月13日20:10:32 石发强