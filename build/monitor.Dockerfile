ARG REG=docker.io
FROM ${REG}/diegofpsouza/numpy:0.0.1

LABEL authors="Wenhui Zhou"

ARG dependency_dir=dependency
ARG lib_dir=dependency/core/lib
ARG base_dir=dependency/core/monitor
ARG code_dir=components/monitor

ENV TZ=Asia/Shanghai

RUN apt-get update && apt-get install -y iperf3 python3-pip

COPY ${lib_dir}/requirements.txt ./lib_requirements.txt
COPY ${base_dir}/requirements.txt ./base_requirements.txt

RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install -r lib_requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip3 install -r base_requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ${dependency_dir} /home/dependency
ENV PYTHONPATH="/home/dependency"

WORKDIR /app
COPY  ${code_dir}/* /app/

CMD ["python3", "main.py"]