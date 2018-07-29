CSV(Comma-Separated Values)即逗号分隔值，可以用Excel打开查看。由于是纯文本，任何编辑器也都可打开。与Excel文件不同，CSV文件中：<br>
* 值没有类型，所有值都是字符串
* 不能指定字体颜色等样式
* 不能指定单元格的宽高，不能合并单元格
* 没有多个工作表
* 不能嵌入图像图表<br>

在CSV文件中，以`,`作为分隔符分隔两个单元格。像这样`a,c`表示单元格`a`和单元格`c`之间有个空白的单元格。依此类推。<br>

不是每个逗号都表示单元格之间的分界。所以即使CSV是纯文本文件，也坚持使用专门的模块进行处理。Python内置了csv模块。先看看一个简单的例子。<br>

### 从CSV文件中读取数据
```python
import csv

filename = 'D:/data.csv'
with open(filename) as file:
    reader = csv.reader(file)
    print(list(reader))
```
`reader`不能直接打印，`list(reader)`最外层是`list`，里层的每一行数据都在一个`list`中，有点像这样
```python
[['name', 'age'], ['Bob', '14'], ['Tom', '23'], ...]
```
于是我们可以这样访问到`Bob`的年龄`reader[1][1]`, 在`for`循环中遍历如下
```
import csv

filename = 'D:/data.csv'
with open(filename) as file:
    reader = csv.reader(file)
    for row in reader:
        # 行号从1开始
        print(reader.line_num, row)
```
截取一部分输出
```python
1 ['AKST', 'Max TemperatureF', 'Mean TemperatureF', 'Min TemperatureF', 'Max Dew PointF', 'MeanDew PointF', 'Min DewpointF', 'Max Humidity', ' Mean Humidity', ' Min Humidity', ' Max Sea Level PressureIn', ' Mean Sea Level PressureIn', ' Min Sea Level PressureIn', ' Max VisibilityMiles', ' Mean VisibilityMiles', ' Min VisibilityMiles', ' Max Wind SpeedMPH', ' Mean Wind SpeedMPH', ' Max Gust SpeedMPH', 'PrecipitationIn', ' CloudCover', ' Events', ' WindDirDegrees']
2 ['2014-1-1', '46', '42', '37', '40', '38', '36', '97', '86', '76', '29.95', '29.77', '29.57', '10', '8', '2', '25', '14', '36', '0.69', '8', 'Rain', '138']
```
