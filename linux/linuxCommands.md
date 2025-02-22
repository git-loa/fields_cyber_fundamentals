***Linux*** is the operating system kernel, which is started by the boot loader, which itself started by the BIOS/UEFI.

1. The kernel ensures coordination between hardware and software.
2. The kernel provides a common base to all programs 
3. Runs in **ring zero** aka **kernel space** 
4. ***The User Space*** is everything that happens outside of the kernel.
5. Linus systems merge all files stores into a single hierarchy.
6. A process is a running instance of a program which requires memory to store both the program itself and its operating data.
7. Kernel is in charge of creating and tracking a process. It assigns a process its **process identifier (PID)**

## Some commands
**ls**: list the content of a directory
- **ls -l**: list the content and permissions of all files in a directory.
- **pwd** the current working directory.
- **echo varialblename**: display content of <varialblename>
- **type** query the type of each command
- **which** reports the location of a given executable
- ***echo "Kali rules!" > kali-rules.txt**: write content to the file "kali-rules.txt"
echo "Kali rules!" >> kali-rules.txt**: append content to the file "kali-rules.txt"
- **cat kali-rules.txt**: display content on screen.
- **find dirname -name filename**: search 
- **grep**:  searches the contents of the files and extracts lines
 matching the regular expression.
- **ps aux**: list the processes currently running 
- **kill -signal pid**: send a signal to a process with PID pid.
- **jobs**
- **chmod rights file**: changes the permissions for the file
- **chown user file**: changes the owner of the file
- **chgrp group file**: changes the group of the file
- **free**: display information on memory
- **df**
- **id**: display identity of the user
- ** uname -a**: display information about the kernel
- **lspci**
- **lsusb**
-  **dmesg**: review kernel logs,
- **journalctl**: show all available logs.
- **wc -l file** count the numer of entries in file


# Configuring and Managing Services
To configure a specific program, 
1. First read the package maintainer's document: '/usr/share/doc/package/README'
2. Look at the software's official documentation.
3. The configuration files are often self-documented.

### Configuring SSH for remote login
**Secure Shell** (SSH) allows one to remotely log into a machine, transfer files, or execute commands.

Connecting to a remote machine: 

```bash
ssh username@remote_host
```
>Exit the seesion with the **exit** command.

>How SSH works: SSH works by connecting a *client program* to an ssh server called ***sshd***. 

Use the command to start the ssh server:
```bash
sudo systemctl start ssh
```

> Configuraion: Configuring SSH means make changes to to the settings of sshd server. The seetings can be changed in the configuration file
>/etc/ssh/sshd_config

> To edit, back up: *sudo cp /etc/ssh/sshd_config{,.bak}*
> Edit using nano or anny preferred text editor: *sudo nano /etc/ssh/sshd_config*
Reload to effect the changes: 
```bash
sudo systemctl reload ssh
```

### How to log into ssh with keys
- Key-based authentication works by creating a pair of keys: a private key and a public key.

- The private key is located on the client’s machine and is secured and kept secret.

- The public key can be given to anyone or placed on any server you wish to access.

- When you attempt to connect using a key pair, the server will use the public key to create a message for the client computer that can only be read with the private key.

- The client computer then sends the appropriate response back to the server, which will tell the server that the client is legitimate.

- This process is performed automatically after you configure your keys.

### Creating SSH keys.
SSH keys should be generated on the computer you wish to log in from. This is usually your local machine.

Enter the following into the command line:
```bash
ssh-keygen -t rsa
```
The commands creates the key pair at the following locations
- ~/.ssh/id_rsa.pub
- ~/.ssh/id_rsa

Tranfer the public key to the server with the following:
1. Using *ssh-copy-id.
```bash
ssh-cpoy-id username@remote_host
```
2. Using SSH (if no ssh-copi-id): We can do this by outputting the content of our public SSH key 
on our local computer and piping it through an SSH connection to the remote server. On the other side, 
we can make sure that the *~/.ssh* directory exists under the account we are using and then output the 
content we piped over into a file called **authorized_keys** within this directory.
```bash
cat ~/.ssh/id_rsa.pub | ssh username@remote_host "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```
Or 
```bash
ssh user@remote_host 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys' < ~/.ssh/id_rsa.pub
```
3. Manually: If you do not have password-based SSH access to your server available, you will have to do the 
above process manually. The content of your **id_rsa.pub file** will have to be added to a file at 
*~/.ssh/authorized_keys* on your remote machine somehow.
```bash 
cat ~/.ssh/id_rsa.pub
```
Create the folder *~/.ssh* on the remote server.
```bash
mkdir -p ~/.ssh
```
Add the content of *~/.ssh/id_rsa.pub* to the the file *~/.ssh/authorized_keys*.
```bash
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```
or
```bash 
echo public_key_string >> ~/.ssh/authorized_keys
```

Disable Password authentication in the */etc/ssh/sshd_config* file, and restart
```bash
sudo systemctl restart ssh
```