# rule-template说明 #

* rule文件有一个dict组成，其中有两个字段，分别是`default` 和`user-def`。分别代表默认规则列表和用户定义规则列表。

* default字段下的数据尽量不要改，唯一可以改的是status字段，当status为false是，规则处于禁用状态

* 用户规则列表由用户规则聚合而成，一个用户规则下的字段包括：

  * `id`: 用户规则id，不能重复

  * `applyScope`: 规则作用域，取值包括"action"(flow中的句子)，"allSentence"(RUCM中所有句子)

  * `simpleRules`: 一个用户规则可以被看做多个简单规则的聚合，简单规则字典信息包括：

    * `subject`: 规则要检查的对象，他的取值包括:

      * subject_Val: 主语的值
      * subject_count：主语的数量
      * object_Val: 宾语的值
      * object_count: 宾语的数量
      * verb_count : 动词的数量
      * verb_tense：动词的时态
      * strs: 句子中所有的词

    * `operation`: 对检查对象的约束，取值可以是“in”,"notIn"

    * `val`： 约束列表，当operation为in 时，所有的检查对象都必须为val中的值之一，当operation为notIn时，所有的检查对象都不能取val中的任何一个值。

      例如`{"subject":"subject_Val","operation":"in","val":["system"]}`表示主语中不能出现system字眼

      列表中除了出现正常字符串以外，还可以出现"$actor"代表RUCM中的actor

  * `status`：当status为false时，规则处于禁用状态

  * `operation`:综合简单规则的逻辑操作

    * 第一个字符代表对整个检查结果的操作"-"代表无操作，"!"代表取非操作
    * 第一个字符往后分别代表对于简单规则之间的逻辑操作，"&"代表与操作，“|”代表或操作
