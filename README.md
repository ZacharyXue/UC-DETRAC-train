# README

主要任务是把 UA-DETRAC 数据集转换成后续需要的格式，涉及到 xml 的读取、zip 解压等等基础的编程，顺便复习一下。

UA-DETRAC数据集链接：https://aistudio.baidu.com/datasetdetail/24530/0 

## ZIP 文件解压

ZIP文件解压使用到 `zipfile` 包：

```python
try:
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(target_directory)
    print(f"成功解压文件：{zip_file_path} 到 {target_directory}")
    return True
except Exception as e:
    print(f"解压文件时出现错误：{e}")
    return False
```
其中：
1. 使用上下文管理器打开zip文件所在的路径
2. 使用 `.extractall()` 方法指定解压路径，解压文件

## `os.path` 的使用

在进行文件操作的时候，`os.path` 是最常使用到的方法，这里简单进行一下整理。

保存文件前通常会检查路径是否存在：
```python
# 检查路径是否存在
if not os.path.exists(target_directory):
    # 不存在则创建对应路径
    os.makedirs(target_directory)
```

想要获取路径中的文件名时可以使用 `os.path.basename()`

拼接路径时可以使用 `os.path.join()`

遍历目录下的所有文件和子目录名称可以使用 `os.listdir(target_directory)`；相比较 `os.walk()` 则会遍历指定目录下的所有文件和子目录，其生成一个迭代器，包含一个三元组：
- `dirpath`：当前遍历的**目录路径**
- `dirnames`：当前目录下的**子目录名称列表**
- `filenames`：当前目录下的**文件名称列表**

## json、xml 的导入导出

json 文件在python中和`dict`相对应，json的导入导出依赖 `json` 包：
```python
with open(json_file_path, 'w') as json_file:
    json.dump(label, json_file)

json.load(json_file)
```

xml的导入之前习惯使用 `xml.etree.ElementTree` 进行，虽然理解起来也还好，但不算方便，最近看到 `xmltodict` ，将 xml 文件也转换为 `dict` 格式，使用方便很多。

```python
with open(xml_file, encoding='utf-8') as fd:
    content = xmltodict.parse(fd.read())
```
上面读取之后，返回一个字典，其中`key`为 XML 中的子节点，`@key` 则是当前节点的属性。理解很直观，当然遍历相对会麻烦些。 

## TODO
- [x] 语法、包的使用
- [ ] 编程解决遇到的问题，反思
- [ ] 假如按照最简洁的函数方式进行转换，该怎么写
- [ ] 如果要更有扩展性，该怎么写
- [ ] 异常打印如何帮助定位
- [ ] 有哪些容易出问题的点 -- 空值，类型（python专属）