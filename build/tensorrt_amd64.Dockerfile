ARG REG=docker.io
FROM ${REG}/yuefan2022/tensorrt-ubuntu20.04-cuda11.6:latest

LABEL authors="Wenhui Zhou"

RUN pip3 install --upgrade pip && \
    pip3 install opencv-python-headless typing_extensions numpy==1.23.1 scipy tiff imagecodecs scikit-learn scikit-image -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip3 --default-timeout=1688 install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117

RUN ["/bin/bash"]