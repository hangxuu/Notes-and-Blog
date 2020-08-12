<!-- GFM-TOC -->
* [二、查询 DSL](#查询DSL)
* [三、参考资料](#参考资料)

<!-- GFM-TOC -->

## 查询 DSL
### 查询上下文和过滤上下文
查询语句的行为取决于它是被用在查询上下文还是过滤上下文。
- 查询上下文
参数“query”后的查询子句用于查询上下文。它回答这样的问题“这个文档与该条查询子句有多匹配？”因为询问程度，因此该查询子句会为每个文档计算一个_score，以代表该文档的匹配度。
- 过滤上下文
参数“filter”后的查询子句用于过滤上下文。它回答这样的问题“这个文档是否匹配这条查询子句？”答案只有两个，是或者不是。不用计算_score。

可想而知。filter的速度肯定要比query快。因此，只有确定需要根据_score来匹配文档的情况下使用查询上下文，其余情况均使用过滤上下文。
例子：
``` python 
{
    "query": {
        "bool": {
            "must": [
                {"match": {"title": "Search"}},
                {"match": {"content": "Elasticsearch"}}
            ],
            "filter": [
                {"term": {"status": "published"}},
                {"range": {"publish_date": {"gte": "2015-01-01"}}}
            ]
        }
    }
}
```
说明：bool和两个match用于查询上下文，term和range用于过滤上下文。
这条查询语句匹配满足以下所有条件的文档：
- title中包含search
- content中包含elasticsearch
- status为published
- publish_date的日期等于2015-01-01或再其之后

### match_all语句
毫无疑问，最简单的语句，匹配所有的文档。
``` python
{
    "query": {
        "match_all": {}
    }
}
```
相反，还有一个”match_none”语句，即一个文档也不匹配。

### 全文查询
#### Match query
``` python
{
    "query": {
        "match" : {
            "message" : "this is a test"
        }
    }
}
```
“message”是字段名，这条query子句在message中匹配[this, is, a, test]，默认使用or，也就是说，“this is a test”它会匹配，“this is a story”它也会匹配，甚至“this”它也会匹配，它们之间的区别，仅在于_score不一样。
如果像下面这样写：
``` python 
{
    "query": {
        "match" : {
            "message" : {
                "query" : "this is a test",
                "operator" : "and"
            }
        }
    }
}
```
“message”是字段名，这条query子句加上了“operator”字段，并设置为“and”，因此它只会匹配“this is a test”，和下面match_phrase的作用一样。
``` python
{
    "query": {
        "match_phrase": {
            "message": "this is a test"
        }
    }
}
```
#### Match phrase query
“match_phrase”匹配短语。见上文。

#### Match phrase prefix query
“match_phrase_prefix”就和“match_phrase”一样，除了它的最后一个单词可以使用前缀查询。
它除了和“phrase”接受相同的参数外，还接受一个“max_expansions”参数（默认为50），表示你输入的最后一个单词往后可以增加多少个字符。
例如：
``` python
{
    "query": {
        "match_phrase_prefix": {
            "message": {
                "query": "quick brown f",
                "max_expansions": 10
            }
        }
    }
}
```
这条query子句会查询“quick brown fox”，“quick brown food”…… 就是说会匹配“message”字段中“quick brown”后接着一个“f”开头单词的文档。 但默认只会查询前50个，这通常不是问题，但还是建议少使用“match_phrase_prefix”，尽量用“match_phrase”进行精确匹配，这样不仅结果更准确，而且效率更高。

#### Multi match query
“multi_match”基于“match”，但支持多领域查询。
例如：
``` python
{
    "query": {
        "multi_match": {
            "query": "this is a test",
            "fields": ["subject", "message"]
        }
    }
}
```
要查询的内容为“this is a test”，在字段“subject”和“message”中进行查询，也就是说，只要文档的“subject”字段或者“message”字段中包含要查询的内容，该文档都会被匹配到。
指定字段时可以使用通配符。例如：
``` python
{
  "query": {
    "multi_match" : {
      "query":    "Will Smith",
      "fields": [ "title", "*_name" ] 
    }
  }
}
```
这条查询子句会在“title”字段，“first_name”字段和“last_name”字段中查询[will, smith]（假设文档存在“first_name”字段和“last_name”字段）。
“multi_match”的类型：
-	best_fields（默认）在每个字段独立匹配所有内容。如上例，则是在“title”字段，“first_name”字段，“last_name”字段分别匹配[will, smith]，并计算得分（因为“will”和“smith”出现在不同的字段意义不大）。
-	most_fields 
-	cross_fields 
-	phrase 当类型选phrase时，查询会用match_phrase而不是match
-	phrase_prefix 当类型选phrase_prefix时，查询会用match_phrase_prefix而不是match

前三种类型，应尽量避免使用，它们的作用很可能和你想象的不一样。
``` python
{
    "query": {
        "multi_match": {
            "query": "this is a test",
            "type": "phrase",
            "fields": ["subject", "message"]
        }
    }
}
```
该例加上了类型“phrase”，因此使用“match_phrase”而不是“match”，即查询“this is a test”而不是[this, is, a, test]。

### Term level查询
#### Term query
``` python
{
  "query": {
    "term" : { "user" : "Kimchy" } 
  }
}
```
这条查询语句匹配字段“user”中存在“Kimchy”的文档。
例如：
``` python
body = {
    "user": "Kimchy",
}
body2 = {
    "user": "kimchy",
}

```
先插入以上两个文档入库，然后执行以上查询语句。结果如下：

![](http://wx1.sinaimg.cn/large/a0f42716gy1fto9k1r0vuj20hn04m74a.jpg)

表示没有匹配到！这是因为文档在入库的时候默认做了分析，无论文档“body”还是“body2”的“user”字段都是小写的“kimchy”，而“term”查询不对所查询的内容做任何分析，所以“Kimchy”得不到任何匹配。
将“term”改为“match”，结果如下：

![](http://wx1.sinaimg.cn/large/a0f42716gy1fto9k6fu7sj20lq05kweo.jpg)

匹配到了全部两个文档且两个文档的分值一样。这是因为“match”在查询前会把“Kimchy”转换为“kimchy”。

#### Terms query
“term”用于查找单个值，当我们想要查找多个值时，就需要用到“terms”查询。这时，我们只需把多个值放到列表里。
例：
``` python
{
    "query": {
        "terms": {"user": ["kimchy", "elasticsearch"]}
    }
}
```
上面这条查询语句匹配“user”字段中包含“kimchy”或者“elasticsearch”的文档。

#### Range query
range查询即范围查询。有四个参数：
-	gte 大于等于
-	gt 大于
-	lte 小于等于
-	lt 小于

例：
``` python
{
    "query": {
        "range" : {
            "age" : {
                "gte" : 10,
                "lte" : 20,
            }
        }
    }
}
```
上面这条query语句匹配“age”字段大于等于10小于等于20的文档。

对于日期的范围查询。
``` python
{
    "query": {
        "range" : {
            "timestamp" : {
                "gte": "2015-01-01 00:00:00", 
                "lte": "now", 
            }
        }
    }
}
```
这条查询语句过滤2015-01-01 00：00：00起至今的文档。

range查询中的时区问题：
例：
``` python
body = {
    "time": "2015-01-01T12:10:30Z",
}
```
上面的时间表示零时区的2015年1月1日12:10:30，这也是ES中默认的时区，也就是说，你写的查询语句会被当成这个时区的时间进行查询（不管你加不加Z）。
如果你查询时写2015-01-01T08:00:40+08:00(东八区)，它会被先转为零时区，然后进行查询。
例：
``` python
# 插入两条文档
body1 = {
    "time": "2015-01-02T00:00:50Z",
}
body2 = {
    "time": "2015-01-02T00:00:30Z",
}
# 执行以下查询语句：
query = {
    "query": {
            "range": {
                "time": {
                    "gte": "2015-01-01T00:00:20Z",
                    "lte": "2015-01-01T23:00:40-01:00"
                }
            }
    }
}
```

结果为文档body2被匹配到。（用西一区做的测试）
![](http://wx3.sinaimg.cn/large/a0f42716ly1ftofvg1v27j20r303ndfv.jpg)
说明：最好的方式是根据文档的时间格式来书写query语句。这样可以避免一些未知的错误。

#### Exists query
exists查询即存在性查询，只有所查询的字段至少存在一个非null值的文档才会被匹配。
``` python
{
    "query": {
        "exists" : { "field" : "user" }
    }
}

# 上面的查询语句会匹配以下文档：
{ "user": "jane" }
{ "user": "" }     # 空字符串不是null
{ "user": "-" } 
{ "user": ["jane"] }
{ "user": ["jane", null ] } 

# 不会匹配以下文档：
{ "user": null }
{ "user": [] }     # []没有值
{ "user": [null] } 
{ "foo":  "bar" }     # 没有“user”字段
```
#### Prefix query
prefix查询（not analyzed）用于前缀查询。
``` python
{ 
    "query": {
        "prefix": { "user": "ki" }
  }
}
```
上面的查询语句匹配“user”字段中存在以“ki”开头的项的文档。

#### Wildcard query
“wildcard”查询（not analyzed，因此，如果要匹配大写，应该保证查询的字段内容也应该为not analyzed），能够让你指定一个模式而不是前缀。它使用标准的shell通配符：
-	？匹配任意字符
-	*匹配零个或者多个字符

``` python
{
    "query": {
        "wildcard": {"user": "ki*y"}
    }
}
```
上面这条query语句能匹配“user”字段内容包含“kitty”，“kizy”，“kibjhfy”……的文档。
要注意的是，通配符查询可能会很慢，而且，应禁止在开头使用*或者？（会更慢）。

#### Regexp query
使用regexp查询能够让你写下更复杂的模式，它的使用方法和wildcard还有prefix都是一样的。
例：下面这条query语句匹配W开头，后接一个0-9的数字，然后再接一个或多个字符的模式。和通配符一样，正则查询可能会很慢。
``` python
{
    "query": {
        "regexp": {
            "postcode": "W[0-9].+"
        }
    }
}
```
#### Type query

type查询根据类型过滤文档。
例：
``` python
{
    "query": {
        "type" : {
            "value" : "_doc"
        }
    }
}
```
这条查询语句匹配所有类型为“_doc”的文档。

#### Ids query
ids查询根据_uid（{type}#{id}的结合体）过滤文档。
例：
``` python
{
    "query": {
        "ids" : {
            "type" : "_doc",
            "values" : ["1", "4", "100"]
        }
    }
}
```
这条查询语句匹配类型为“_doc”，“id”为1，4，100的文档。“type”字段可以省略。

### 复合查询
#### Bool query
``` python
{
  "query": {
    "bool" : {
      "must" : {
        "term" : { "user" : "kimchy" }
      },
      "filter": {
        "term" : { "tag" : "tech" }
      },
      "must_not" : {
        "range" : {
          "age" : { "gte" : 10, "lte" : 20 }
        }
      },
      "should" : [
        { "term" : { "tag" : "wow" } },
        { "term" : { "tag" : "elasticsearch" } }
      ] 
    }
  }
}
```
“must” - 必须满足。对于上例： “user”字段必须包含“kimchy”。
“filter” - 过滤。对于上例：在“tag”字段值为“tech”的文档中进行查询。
“must_not” - 必须不满足。对于上例：不要年龄字段在[10, 20]岁的文档。
“should” - 应该满足。对于上例： 完全没用，只影响分数。
如果bool语句是查询上下文，那么只要查询子句中有“must”，或者“filter”，“should”就只影响分数。如果查询子句中既没有“must”也没有“filter”或者bool语句是过滤上下文，那么文档必须满足“should”中的一个条件才能被匹配。

#### Dix max query
建议：能使用bool查询尽量使用bool查询，bool查询效果不理想时再考虑dis_max查询。
我在网上找到了一篇写的很好又详细的博文，这里就不再赘述，地址如下：[https://blog.csdn.net/dm_vincent/article/details/41820537](https://blog.csdn.net/dm_vincent/article/details/41820537)。
说明：我用ES6.x测试博主的例子，结果并不完全一致，可以看出ES对于匹配算法做了一些改进，但基本不影响博主的分析。

### Nested query
关于nested query，其实在nested类型那块已经说的差不多了。这里再说一个例子。
``` python
# mapping 设置
{
    "mappings": {
        "type1" : {
            "properties" : {
                "obj1" : {
                    "type" : "nested"
                }
            }
        }
    }
}
```
这里字段“obj1”被设置为“nested”类型。
``` python
# query语句
{
    "query": {
        "nested" : {
            "path" : "obj1",
            "query" : {
                "bool" : {
                    "must" : [
                    { "match" : {"obj1.name" : "blue"} },
                    { "range" : {"obj1.count" : {"gt" : 5}} }
                    ]
                }
            }
        }
    }
}
```
“path：obj1”是说在“obj1”字段中查询。
“obj1”包含一个数组，这条查询语句要求对数组中的每一项，至少有一项的“name”字段值为“blue”，同时“count”字段值大于5。而不是数组中一项的“name”字段值为“blue”，而另一项的“count”字段值大于5。

还是用数据说明吧。
先放两条文档入库：
``` python
body = {
    "obj1": [
        {
            "name": "blue",
            "count": 6
        },
        {
            "name": "yellow",
            "count": 9
        }
    ]
}
body2 = {
    "obj1": [
        {
            "name": "blue",
            "count": 2
         },
        {
            "name": "yellow",
            "count": 6
        }
    ]
}
```
然后执行上面的query语句。程序执行结果如下：

![](http://wx4.sinaimg.cn/large/a0f42716gy1fto9k8z6qyj20k4052glo.jpg)

可以看出，该query语句只匹配了第一个文档body，而没有匹配第二个文档body2。符合我上面的解释。

## 参考资料

- [终于有人把Elasticsearch原理讲透了！](https://zhuanlan.zhihu.com/p/62892586)

