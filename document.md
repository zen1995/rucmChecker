# 针对RUCM需求的checkstyle@敏敏特穆尔

## 1. 提交文件的说明
本组开发了针对RUCM模型的checkstyle工具用于检查RUCM模型文件的合法性与否，其主要功能是帮助用户检查其开发的RUCM设计模型是否符合RUCM设计要求的26条规则与其它用户指定的默认规则。
提交的主要文件有：
1. 代码部分
2. UML设计模型，包含类图与时序图等，通过StarUML软件导出的JPG格式图片与mdj格式模型文件两种方式提供，位于src目录下
3. OCL、rucm规则模板、原始的领域分析报告等文件，位于doc目录下

## 2.代码运行指南

(1) 本项目基于自然语言处理算法在C/S架构下开发，自然语言处理部分使用了现有AI算法，尚有不完美之处，因此本部分可能会出现部分不可控bug，如自然语句在分词操作中出现分不开的现象，请大家谅解。这里自然语言处理服务我们已经部署到了校内服务器供大家直接调用，在远程服务器不稳定或失效的情况下请大家在本地部署自然语言处理服务程序。操作如下：  
   ```bash
    # 首先下载相关的文件，如果下载速度太慢的，北航校园网下可以去"ftp://10.111.1.29/share-folder"里下载stanford-corenlp-full-2018-10-05.zip
    wget https://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip
    # 解压后，cd到其文件夹内，然后执行服务启动命令，其中端口可以修改
    java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
   ```
(2) 我们的系统以main函数问入口，如果要测试请执行如下命令：  
   ```bash
    python3 main.py -h
    # 其中-h参数用于显示帮助信息
   ```
   完整的用法示例如下：
   ```bash
    python main.py -u http://10.133.6.180:9000/ -r ./test/rule-template.txt ./test/test.rucm
   ```