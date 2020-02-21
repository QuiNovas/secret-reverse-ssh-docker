FROM python:3.7-slim

COPY entrypoint.py /entrypoint.py

RUN chmod +x /entrypoint.py && \
    pip3 install boto3 botocore && \
    apt update && \
    apt -y install openssh-client bash && \
    useradd -s /bin/false sshuser && \
    mkdir -p /home/sshuser/.ssh

RUN chown -R sshuser:sshuser /home/sshuser/

USER sshuser

CMD /entrypoint.sh
