import json
import os
import subprocess
import shlex


def describe_instances():
    command = 'aws ec2 describe-instances --region=ap-northeast-1 '\
        '--filter="Name=instance-state-name,Values=running"'

    cmd_res = subprocess.run(shlex.split(command), stdout=subprocess.PIPE)
    return json.loads(cmd_res.stdout)


def get_instance_name(instance):
    name = None
    tags = instance['Tags']
    for tag in tags:
        if tag['Key'] == 'Name':
            name = tag['Value']
    return name


def get_instance_private_ip(instance):
    return instance['NetworkInterfaces'][0]['PrivateIpAddress']


def build_config_text(instance_name, private_ip):
    return f"""
Host {instance_name}
  User root
  Port 22
  HostName {private_ip}
  IdentityFile ~/.ssh/jaaxman
  TCPKeepAlive yes
  IdentitiesOnly yes
  StrictHostKeyChecking no
  UserKnownHostsFile=/dev/null
"""


def write_ssh_config(config_texts):
    path = os.path.join(os.path.expanduser('~'), '.ssh', 'config')
    with open(path, 'w') as f:
        for text in config_texts:
            f.write(text)
    os.chmod(path, 0o644)


if __name__ == '__main__':
    result = describe_instances()
    config_texts = []
    for instance_info in result['Reservations']:
        for instance in instance_info['Instances']:
            name = get_instance_name(instance)
            if name is None or not name.startswith('jaaxman') or name == 'jaaxman-gateway':
                continue
            private_ip = get_instance_private_ip(instance)
            config_texts.append(build_config_text(name, private_ip))

    write_ssh_config(config_texts)
    print('update ssh-config.')
