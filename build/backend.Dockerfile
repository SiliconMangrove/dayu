ARG REG=docker.io
FROM ${REG}/python:3.8

LABEL authors="Wenhui Zhou"

ARG dependency_dir=dependency
ARG lib_dir=dependency/core/lib
ARG code_dir=backend

ENV TZ=Asia/Shanghai

COPY ${lib_dir}/requirements.txt ./lib_requirements.txt
COPY ${code_dir}/requirements.txt ./code_requirements.txt

RUN pip3 install --upgrade pip && \
    pip3 install -r lib_requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip3 install -r code_requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ${dependency_dir} /home/dependency
ENV PYTHONPATH="/home/dependency"

WORKDIR /app
COPY  ${code_dir}/* /app/

CMD ["python3", "main.py"]
