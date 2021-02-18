## 数据处理流程
1. csv/excel 文件 ——> 提取出数据格式到dict中，提取出其中的ISBN，和基础信息
2. 将每一个ISBN按顺序经过queryer进行查询，如果一个查不到，再查第二个
3. 确定queryer的具体查询目标，对不同的API有指定的字段, 父类Queryer类，子类就是不同的Queryer
   需要实现queryBook接口和parse接口
4. 将查询得到的数据结构，重新放回原来的数据源中，生成一个新的csv文件

## 其中所需要复习的技术
1. 如何优雅的使用requests，设定get,post的body与header
2. 如何解析json格式文件，应该如何存放这些json格式文件，dict 还是 类？
3. csv/excel文件的读取与写入
4. 如有必要，需要一个网站的实现，能够实时读取
5. Python中父类与子类的关系