```bash
python3 main.py --help
```
## dependency setup
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

## pdf generator install

Download the tool from [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html).
Add the binary executable to environment varible `PATH`.

## ToDoList
- [x] 代码开发
- [x] Demo结果
- [x] newest design of model
- [x] OCl  
--by shifaqiang
- [x] 中文RUCM文件的分词与解释，请小帅哥杨森考虑能否实现，调查现有的中文分词工具
- [x] 规则的再抽象与理解，实现规则的可扩展性，最帅的泽年继续设计呀
- [x] 输出界面的美化，请审美小公主梁保宇考虑如何构造美丽的界面
- [x] 运行过程全盘云端化，通过浏览器进行访问与展示，最丑陋的发强想办法
- [x] 请子粤调研Python后端的web开发，尝试连接服务器与前端展示页面，主要沟通梁保宇  
-- 2018年12月13日20:10:32 石发强
- [ ] 修改用户规则程序崩溃的问题（泽年）
- [ ] 点击规则检查按钮之后的程序应该有正在检查、检查完成、查看报告的流程按钮，不能没有任何提示（子粤，鲍鱼）
- [ ] 实现check方法（杨森）
- [ ] 查看报告是空白的（泽年）
- [ ] 测试中文会直接报错，保证中文可以检查（杨森）
- [ ] 界面样式合规审查（鲍鱼）
- [ ] 更新UI设计与规则抽象、中文语言支持等方面的设计类图（更新类图泽年总负责，杨森和鲍鱼协助）
- [ ] 最终答辩报告与PPT（发强，与助教师兄约见之后确定）  
-- 以上内容请在2018年12月23日晚上12点之前完成，周一必须约助教演示一遍（2018年12月22日14:47:41，石发强）