#!/usr/bin/env python3.7
from os import environ as env, system
from base64 import b64decode as b64
import boto3

if "SSH_PORT" not in env: env["SSH_PORT"] = "443"
if "SSH_USER" not in env: env["SSH_USER"] = "appliance"
if "SSH_SERVER" not in env: env["SSH_SERVER"] = "localhost"
if "REMOTE_PORT" not in env: env["REMOTE_PORT"] = "8443"
if "LOCAL_PORT" not in env: env["LOCAL_PORT"] = "8443"
if "SSH_OPTIONS" not in env: env["SSH_OPTIONS"] = ""
if "DESTINATION_SERVER" not in env: env["DESTINATION_SERVER"] = "localhost"
if not set(["PRIVATE_KEY_SECRET", "SERVER_HOST_KEY_SECRET"]) & set(env):
    raise ValueError("You must set PRIVATE_KEY_SECRET and SERVER_HOST_KEY_SECRET as environment variables")

def listSecrets():
    c = boto3.client('secretsmanager')
    r = c.list_secrets(MaxResults=100)
    secrets = [l["Name"] for l in r["SecretList"]]
    while "NextToken" in r and r["NextToken"] and r["NextToken"] is not None:
        r = c.list_secrets(MaxResults=100, NextToken=r["NextToken"])
        secrets = [l["Name"] for l in r["SecretList"]] + secrets
    return secrets

def getKeys():
    c = boto3.client('secretsmanager')
    secrets = listSecrets()
    if set([env["PRIVATE_KEY_SECRET"], env["SERVER_HOST_KEY_SECRET"]]) & set(secrets):
        key = c.get_secret_value(SecretId=env["PRIVATE_KEY_SECRET"])["SecretString"]
        serverKeys = c.get_secret_value(SecretId=env["SERVER_HOST_KEY_SECRET"])["SecretString"]
        system("rm -f /home/sshuser/.ssh/id_rsa")
        with open("/home/sshuser/.ssh/id_rsa", "w") as f:
            f.write(b64(key).decode())
            system("chmod 0400 /home/sshuser/.ssh/id_rsa")
        with open("/home/sshuser/.ssh/known_hosts", "w") as f:
            f.write(b64(serverKeys).decode())
            system("chmod 0644 /home/sshuser/.ssh/known_hosts")
    else:
        msg = "Either private or public keys. Exiting"
        raise SystemExit(msg)

def ssh():
    if "TIMEOUT" in env and env["TIMEOUT"]: timeoutCmd = f"""timeout -k {env["TIMEOUT"]} """
    else: timeoutCmd = ""
    cmd = f"""{timeoutCmd} ssh -vi /home/sshuser/.ssh/id_rsa -o BatchMode=no -o HashKnownHosts=no {env["SSH_OPTIONS"]} -NT -p{env["SSH_PORT"]} -R{env["REMOTE_PORT"]}:{env["DESTINATION_SERVER"]}:{env["LOCAL_PORT"]} {env["SSH_USER"]}@{env["SSH_SERVER"]}"""
    system(cmd)


getKeys()
ssh()
