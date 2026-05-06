# 2026-YOLO-World-MMKit

基于[AILab-CVC/YOLO-World](https://github.com/AILab-CVC/YOLO-World)项目分支而来。

## 你为什么需要这个？

我正在一个项目中使用YOLO-World，但由于复杂的依赖关系和过时的mmcv环境，[官方GitHub仓库](https://github.com/AILab-CVC/YOLO-World)使用起来非常困难。你可能会说用Ultralytics不好吗？确实，它是一个非常方便且实用的平台。你可以通过[ultralytics/models/yolo-world/](https://docs.ultralytics.com/zh/models/yolo-world/)轻松使用YOLO-World。

然而，在自定义YOLO-World时，我们仍然需要使用`mmcv`、`mmengine`和`mmyolo`来加载模型和预训练权重，而不能直接通过Ultralytics。因此，最终你还是需要处理依赖关系和环境问题。

在这个项目中，我试图改变现状。不仅要让YOLO-World像Ultralytics上的模型一样易于使用，还要使其便于定制。

## 清单

- [x] 移植“configs”
- [x] 移植“yolo_world”
- [x] 移植“tools”
- [_] 移植“导出oonx”

- [x] 环境构建文档
- [ ] 使用文档
- [ ] 迁移学习文档

## 文件

### 我的工作

#### 如何使用？

首先搭建好环境，然后填写配置文件并加载数据集，之后使用工具进行训练、验证或者测试，最后使用demo对输出进行尝试。

#### 环境

我的选择是使用Docker来安装mmcv，我建议你同样采用这种方式，除非你想学习如何构建环境。你可以使用Ubuntu服务器或`Windows Subsystem for Linux`（wsl2）来运行Docker。
- 位置：     [env/](env/) 
- 自述文件：  [here](env/readme.md)

#### 配置

由于文件结构发生了变化，我编辑了一些配置文件，以使其更具灵活性。
- 位置：     [configs/](configs/) 
- 自述文件：  [here](configs/readme.md)

此外，我还将class_text_path移动到了configs文件夹中。 
- 位置：     [configs/data_text_json](configs/data_text_json/) 
- 自述文件：  [here](configs/data_text_json/readme.md)

### 原作

我保存了所有原始代码，以表达对YOLO-World团队的敬意。
- 位置：          [Original/](Original/) 
- 自述文件：       [here](Original/readme.md) 
- 详细信息（必读）：[here](Original/originaldetail.md)