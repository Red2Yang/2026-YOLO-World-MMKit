# Dockerfile build

build：

```
docker build -t YOLO-World-MMkit-env .
```

run:

```
docker run --gpus all -it\
  -v /path/to/YOLO-World-MMkit:/workspace \
  -w /workspace \
  YOLO-World-MMkit-env \
  /bin/bash
```