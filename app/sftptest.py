import paramiko
ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect('86.62.248.233', username='2736798986565656', password='Tests@34s#', key_filename='\download\2736798986565656.ppk')

stdin, stdout, stderr = ssh.exec_command('ls')
print (stdout.readlines())
ssh.close()