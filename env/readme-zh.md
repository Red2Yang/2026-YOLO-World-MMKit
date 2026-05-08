# Dockerfile 构建环境使用方法

中文版本

## 驱动

如果你是第一次使用`cuda`的`docker`镜像，那么请先安装`NVIDIA Container Toolkit`。

在`Ubuntu`系统环境中运行：

```
# 检查是否有系统驱动
nvidia-smi
# 检查是否有docker
docker -v
# Ubuntu
# 配置源
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update

# 安装
sudo apt-get install -y nvidia-container-toolkit

# 重启Docker服务
sudo systemctl restart docker
```

## 使用

构建：

```
docker build -t yw-env .
```

运行：

```
docker run --gpus all -it \
  -v /path/to/YOLO-World-MMkit:/workspace \
  -w /workspace \
  yw-env \
  /bin/bash
```

之后你可以使用`docker exec -it YOLO-World-MMkit-env /bin/bash`再次进入容器。

### 下载组件

Dockerfile内没有拷贝或下载`mmyolo`代码、`YOLO-World`代码及`huggingface`模型，需要你自行下载并挂载。

`mmyolo`代码、`YOLO-World`代码都已经在仓库中了，挂载到容器内即可。

`huggingface`下载：

```
# 先添加“HF_ENDPOINT=https://hf-mirror.com”到环境变量，这样会使用镜像源下载。
python3 -c "from transformers import CLIPTokenizer; CLIPTokenizer.from_pretrained('openai/clip-vit-base-patch32')"
# 下载位置"~/.cache/huggingface"，将/huggingface文件夹挂载到容器内后
cp ./huggingface ~/.cache/huggingface
```

如果要使用本地CLIP模型，需要下载后修改`configs/`内的配置文件，修改`text_model_name`的位置。

### 安装`mmyolo`和`YOLO-World`

在`/workspace/utils/mmyolo/`运行`pip3 install -e .`以安装`mmyolo`。

```
# 找不到可以确保添加sys.Path
echo 'export PYTHONPATH=/workspace:/workspace/path/to/mmyolo:$PYTHONPATH' >> ~/.bashrc
source ~/.bashrc
```

在`/workspace/src/`运行`pip3 install -e .`以安装`YOLO-World`。

```
# 找不到可以确保添加sys.Path
echo 'export PYTHONPATH=/workspace:/workspace/path/to/src:$PYTHONPATH' >> ~/.bashrc
source ~/.bashrc
```