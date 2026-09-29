# hadolint ignore=DL3007
FROM alpine:3.24.2

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

# hadolint ignore=DL3018
RUN apk add --no-cache \
      bash \
      curl \
      iproute2 \
      iputils \
      net-snmp \
      net-snmp-tools \
      openssh-server \
      python3 \
      sudo && \
    adduser -D -s /bin/bash student && \
    echo 'student:student' | chpasswd && \
    printf 'student ALL=(ALL) NOPASSWD: ALL\n' > /etc/sudoers.d/student && \
    chmod 0440 /etc/sudoers.d/student && \
    printf 'PasswordAuthentication yes\nPermitRootLogin no\n' > /etc/ssh/sshd_config.d/cms-labs.conf

COPY snmpd.conf /etc/snmp/snmpd.conf
COPY lab_agent.py /usr/local/bin/lab-agent
COPY entrypoint.sh /usr/local/bin/lab-node-entrypoint

RUN chmod 0755 /usr/local/bin/lab-agent /usr/local/bin/lab-node-entrypoint

EXPOSE 22/tcp 161/udp 8080/tcp

HEALTHCHECK --interval=5s --timeout=2s --retries=12 \
  CMD ["curl", "--fail", "--silent", "http://127.0.0.1:8080/healthz"]

ENTRYPOINT ["/usr/local/bin/lab-node-entrypoint"]
