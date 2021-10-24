import os
import paramiko
from multiprocessing import Process


class ExportPrepare(object):
    def __init__(self):
        self.ip = 'xx.xxx.xxx.xxx'
        self.port = 22
        self.username = 'root'
        self.password = ''

    def sftp_con(self):
        t = paramiko.Transport((self.ip, self.port))
        t.connect(username=self.username, password=self.password)
        return t

    # Find all the directories you want to upload already in files.
    def __get_all_files_in_local_dir(self, local_dir):
        all_files = list()

        if os.path.exists(local_dir):
            files = os.listdir(local_dir)
            for x in files:
                filename = os.path.join(local_dir, x)
                if filename == 'C:/Users/Hang Yang/Desktop/novels\\novel-original':
                    continue
                print "filename:" + filename
                # isdir
                if os.path.isdir(filename):
                    all_files.extend(self.__get_all_files_in_local_dir(filename))
                else:
                    all_files.append(filename)
        else:
            print '{}does not exist'.format(local_dir)
        return all_files

    # Copy a local file (localpath) to the SFTP server as remotepath
    def sftp_put_dir(self):
        try:
            # Upload the local test directory to remote root / usr / below
            local_dir = "C:/Users/Hang Yang/Desktop/novels"
            remote_dir = "/www/wwwroot/xx.xxx.xxx.xxx"

            t = self.sftp_con()
            sftp = paramiko.SFTPClient.from_transport(t)

            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.ip, port=self.port, username=self.username, password=self.password, compress=True)
            ssh.exec_command('rm -rf ' + remote_dir)
            if remote_dir[-1] == '/':
                remote_dir = remote_dir[0:-1]
            all_files = self.__get_all_files_in_local_dir(local_dir)
            for x in all_files:
                filename = os.path.split(x)[-1]
                remote_file = os.path.split(x)[0].replace(local_dir, remote_dir)
                path = remote_file.replace('\\', '/')
                # The MKDIR that creates the directory SFTP can also be used,
                # but can't create a multi-level directory, so use SSH to create.
                p = Process(target=self.ssh_operations, args=(path, ssh, filename, sftp, x))
                p.run()
                p.join()
            ssh.close()

        except Exception, e:
            print e

    def ssh_operations(self, path, ssh, filename, sftp, x):
        tdin, stdout, stderr = ssh.exec_command('mkdir -p ' + path)
        print stderr.read()
        remote_filename = path + '/' + filename
        print u'Put files...' + filename
        sftp.put(x, remote_filename)


if __name__ == '__main__':
    export_prepare = ExportPrepare()
    export_prepare.sftp_put_dir()
