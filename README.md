#Secret Reverse SSH
##Creates a configurable reverse ssh tunnel using AWS secrets for keys

```
    ENV VARS:
      SSH_PORT - ssh port on the remote server
      SSH_USER - user to ssh into the remote server as (default: sshuser)
      SSH_SERVER - the server to ssh into
      REMOTE_PORT - the port on the server that will be forwarded to us
      LOCAL_PORT - the local port traffic from the ssh server will be delivered to
      SSH_OPTIONS - a string of ssh options (-o SomeOption=foo -o AnotherOption=yes)
      DESTINATION_SERVER - the server that LOCAL_PORT traffic will be sent to
      PRIVATE_KEY_SECRET - the name of the AWS secret that our private key is in.
      SERVER_HOST_KEY_SECRET - name of the AWS secret that our trusted public host key is in.
```

The service will ssh into SSH_SERVER and set up a listening port on REMOTE_PORT all traffic on the server will be forwarded
back to the container. If DESTINATION_SERVER is empty then traffic will be delivered to localhost in the container. If set
then traffic from the remote server will be sent to DESTINATION_SERVER. You will also need to pass your AWS credentials into
the container(AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, AWS_DEFAULT_REGION)

##Note on keys:
The private key and server host key must be base64 encoded. If they don't both exist then the process will exit with an error

##EXAMPLES:
Forward traffic from port 443 on the server to 443 on localhost:
```
    docker run -d \
    --rm \
    -e PRIVATE_KEY_SECRET=my-private-key \
    -e SERVER_HOST_KEY_SECRET=my-server-host-pub \
    -e REMOTE_PORT=443 \
    -e LOCAL_PORT=443
    -e AWS_DEFAULT_REGION=us-east-1 \
    -e AWS_ACCESS_KEY_ID=*************\
    -e AWS_SECRET_ACCESS_KEY=************** \
    quinovas/secret-reverse-ssh:latest
```

Run nginx in a container and forward all traffic on port 8080 from the server to it:
```
    docker network create test-net

    docker run -d \
    --rm \
    --net=test-net \
    --name=nginx \
    --expose 8080 \
    nginx:latest

    docker run \
    --rm \
    -e PRIVATE_KEY_SECRET=my-private-key \
    -e SERVER_HOST_KEY_SECRET=my-server-host-pub \
    -e REMOTE_PORT=8080 \
    -e LOCAL_PORT=8080
    -e DESTINATION_SERVER=nginx \
    -e AWS_DEFAULT_REGION=us-east-1 \
    -e AWS_ACCESS_KEY_ID=*************\
    -e AWS_SECRET_ACCESS_KEY=************** \
    quinovas/secret-reverse-ssh:latest    
```
