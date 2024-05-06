#! /usr/bin/env python
import paramiko


class SSH():
    def __init__(self, username, hostname, password, FILEPATH, FILENAME):
        self.username = username
        self.hostname = hostname
        self.password = password
        self.filepath = FILEPATH
        self.filename = FILENAME
        self.BaseCommand = 'source /opt/ros/kinetic/setup.bash && source ~/catkin_ws/devel/setup.bash'
        self.command = None
        self.stdout = None
        self.ssh = None
    def ConnectSSH(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.ssh.load_system_host_keys()

        self.ssh.connect(self.hostname, username=self.username, password=self.password)
        print('connected')
        return self.ssh
    def SendCommand(self, command):
        ssh = self.ConnectSSH()
        command = self.BaseCommand + '&&' + self.filepath + '/' + self.filename + ' ' + command
        print('executing:')
        print(command)
        stdin, self.stdout, stderr = ssh.exec_command(command)
        #stdin, self.stdout, stderr = ssh.exec_command(command)

        self.stdout = self.stdout.read().decode('utf-8')
        print(self.stdout)
        print(stderr.read().decode('utf-8'))
        #print(stdin.read().decode('utf-8'))
        ssh.close()


def main():
    username = 'baherkherbek'
    #hostname = '169.254.200.200'
    hostname = 'raspberrypi.local'
    password = 'qqq'

    client = SSH(username, hostname, password, 'Desktop/master', 'handler.py')
    client.command = 'Move 0.16 0 0.35 0 0 0'
    client.SendCommand()




if __name__ == "__main__":
    main()
