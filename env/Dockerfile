FROM nvcr.io/nvidia/cuda:11.6.2-devel-ubuntu20.04

ENV FORCE_CUDA="1"
ENV MMCV_WITH_OPS=1

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip     \
    libgl1-mesa-glx \
    libsm6          \
    libxext6        \
    libxrender-dev  \
    libglib2.0-0    \
    git             \
    python3-dev     \
    python3-wheel   \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip \
        --retries=5 \
    && pip3 install \
        gradio \
        opencv-python==4.10.0.84 \
        supervision \
        mmengine==0.10.7 \
        setuptools==60.2.0 \
        openmim==0.3.9 \
        --retries=5

# install PyTorch 1.12.0 + CUDA 11.6
RUN pip3 install --no-cache-dir \
    torch==1.12.0+cu116 \
    torchvision==0.13.0+cu116 \
    --extra-index-url https://download.pytorch.org/whl/cu116 #--default-timeout=100 (use it if your network is not fast)

# install MMCV 2.0.1
RUN pip3 install --no-cache-dir \
    mmcv==2.0.1 -f https://download.openmmlab.com/mmcv/dist/cu116/torch1.12.0/index.html

# install MMDetection 3.2.0
RUN pip3 install mmdet==3.2.0

# install transformers
RUN pip3 install transformers

CMD ["/bin/bash"]