FROM python:3.7-slim

RUN pip3 install boto3 botocore && \
    apt update && \
    apt -y install openssh-client bash && \
    useradd -s /bin/false sshuser && \
    mkdir -p /home/sshuser/.ssh


COPY entrypoint.py /entrypoint.py

RUN chown -R sshuser:sshuser /home/sshuser/ && \
    chmod +x /entrypoint.py

USER sshuser

CMD /entrypoint.py
