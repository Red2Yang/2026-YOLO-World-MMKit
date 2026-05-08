# Dockerfile build

[switch to Chinese](readme-zh.md)

## how to use

build：

```
docker build -t yw-env .
```

run:

```
docker run --gpus all -it \
  -v /path/to/YOLO-World-MMkit:/workspace \
  -w /workspace \
  yw-env \
  /bin/bash
```