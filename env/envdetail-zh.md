# Dockerfile 构建环境使用方法

中文版本

构建：
```
docker build -t YOLO-World-MMkit-env .
```

运行：
```
docker run --gpus all -it\
  -v /path/to/YOLO-World-MMkit:/workspace \
  -w /workspace \
  YOLO-World-MMkit-env \
  /bin/bash
```

## 进入容器后事项：

### 下载组件

Dockerfile内没有拷贝或下载`mmyolo`代码、`YOLO-World`代码及`huggingface`模型，需要你自行下载并挂载。

`mmyolo`代码、`YOLO-World`代码都已经在仓库中了，挂载到容器内即可。

`huggingface`下载：

```
# 先添加“HF_ENDPOINT=https://hf-mirror.com”到环境变量，这样会使用镜像源下载。
python3 -c "from transformers import CLIPTokenizer; CLIPTokenizer.from_pretrained('openai/clip-vit-base-patch32')"
# 下载位置"~/.cache/huggingface"，将huggingfacewen文件夹挂载到容器内后
cp ./huggingface ~/.cache/huggingface
```

### 安装`mmyolo`和`YOLO-World`

在`/workspace/utils/mmyolo/`运行`pip3 install -e .`以安装`mmyolo`。

```
# 确保添加sys.Path
echo 'export PYTHONPATH=/workspace/YOLO-World:/workspace/YOLO-World/third_party/mmyolo:$PYTHONPATH' >> ~/.bashrc
source ~/.bashrc
```

在`/workspace/src/`运行`pip3 install -e .`以安装`YOLO-World`。