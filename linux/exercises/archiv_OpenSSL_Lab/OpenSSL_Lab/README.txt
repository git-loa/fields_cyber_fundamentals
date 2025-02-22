Exercise: Password Management Strategies with OpenSSL
------------------------------------------------------
Bash files: 
1. encrypt_random32_string.sh
2. encrypt_secret.sh
3. share_bob.sh
4. test_share_bob.sh

-----------------------------------------------------
Task 1: Create a working directory called OpenSSL_Lab
-----------------------------------------------------
The exercise begins by creating a folder called "OpenSSL_Lab". This folder contains all files and other subdirectories.


----------------------------
Task 2: Write a bash command
----------------------------
The command is: 

echo "Enter name of the output file with extension .enc: " && \
read output_file && \
mkdir -p Passwords && \
read -sp "Enter password: " password && echo && \
openssl rand -hex 32 | openssl enc -aes-256-cbc -pbkdf2 -salt -iter 64000 -md sha256 -pass pass:"$password" -out "Passwords/${output_file}"
unset password

- The command ask for a file with extension .enc
- Passwords subdirectory is created if it does not exist.
- The command again ask for the master password, which is first secure password provided in the Exercise.
  The password is stored in a variable password temporarily in memory. 
- The fires opessl creates a random hex string of size 32,. It is piped to the second openssl 
  command together with the password.  
- Output is a file "file_output" containing the encrypted 32 hex-string.
- Finally the command unsets the variable. That, it clears it from memory.


The encryption uses the cipher: aes-256-cbc.
Options: -pbkdf2, -salt, -iter 64000 and -md sha256

---------------------------------------------------------------------------
Task 3: Use your command to create 3 different aes-256-cbc encrypted files 
---------------------------------------------------------------------------
The command in Task 2 is executed three times to create the following files. Each execution requires a file name. 
	1. password1.enc
	2. password2.enc
	3. password3.enc



--------------------------------------------------------------------------- 
Task 4: Create 3 text files named secret1.txt, secret2.txt, and secret3.txt
---------------------------------------------------------------------------
The three files are created with the following commands:

First create the subdirectory Plaintexts inside OpenSSL_Lab/ using the command: "mkdir Plaintexts". Navigate to Plaintexts and create the files.

echo -n "This is my first secret." > secret1.txt
echo -n "This is my second secret." > secret2.txt
echo -n "This is my third secret." > secret3.txt



-----------------------------------------------------------------------------------
Task 5: Encrypt each of these files using openssl enc, with the cipher -aes-128-ctr
-----------------------------------------------------------------------------------
#!/bin/bash

# Create directory for storing encrypted files 

mkdir -p Ciphertexts && \
for i in {1..3}; do
  # Decrypt the password and use it to encrypt the secret files
  read -sp "Enter password for file password${i}.enc: " password && echo
  decrypted_password=$(echo $password | openssl enc -d -aes-256-cbc -pbkdf2 -salt -iter 64000 -pass stdin -in Passwords/password${i}.enc -md sha256 | tr -d '\n')
  
  if [ -z "$decrypted_password" ]; then
    echo "Decryption failed for password${i}.enc"
    continue
  fi
  openssl enc -aes-128-ctr -pbkdf2 -iter 64000 \
  -in Plaintexts/secret${i}.txt -out Ciphertexts/encrypted_secret${i}.enc \
  -pass pass:"$decrypted_password"
  
  unset password decrypted_password
done


Each file OpenSSL_Lab/Plaintexts/secret{i}.txt is encrypted with the corresponding file OpenSSL_Lab/Passwords/password{i}.enc as follows:
First
	- Create the folder "Ciphertexts" with the command if it does not exist: "mkdir -p Ciphertexts"
	- use the cipher -aes-128-ctr together with the options -pbkdf2 -iter 64000 for the encryption.
	- Read the password used in Task 3 from standard input and pass it to openssl each. 
	- Use a for to loop through the subfolders "Plaintexts" and "Passwords" 
	- So, for the first loop, i=1 and the file "secret1.txt" is selected from "Plaintexts". The file "password1.enc"
	  is also selected. It is decrypted using the cipher from Task 3 and stored in a variable called "decrypted_password".
	  This is used together with the cipher "-aes-128-ctr together with the options -pbkdf2 -iter 64000" to encrypt secret1.txt and the output
	  is saved as "OpenSSL_Lab/Ciphertexts/encrypted_secret1.enc". The process is repeated for "secret2.txt" and "secret3.txt" through the for loop.
	- The if statement is to ensure that the "$decrypted_password" is not empty.
	- Again unset the variables password and decrypted_password
	


-------------------------------------------------------------------------------------------------
Task 6: Decrypt password2.enc and then re-encrypt it with the password 
-------------------------------------------------------------------------------------------------
read -sp "Enter master password: " master_password && echo && \
read -sp "Enter password to share file with Bob: " file_password && echo && \
openssl enc -d -aes-256-cbc -salt -pbkdf2 -iter 64000 -pass pass:"${master_password}" -in Passwords/password2.enc \
-md sha256 | openssl enc -aes-256-cbc -salt -pbkdf2 -iter 64000 -pass pass:"${file_password}" -md sha256 \
-out Passwords/password2_4Bob.enc





1. Decrypt password2.enc with following: 
	openssl enc -d -aes-256-cbc -pbkdf2 -salt -iter 64000 -pass file:pass.txt -in Passwords/password2.enc -md sha256

2. Pipe the Decrypted Password: 
	The output of the decryption is piped (|) directly into the next command, avoiding saving the plaintext to disk.

3. Re-encrypt with Bob's Password:
	openssl enc -aes-256-cbc -pbkdf2 -salt -iter 64000 -pass pass:SuperSecurePassword4Bob -md sha256 -out Passwords/password2_4Bob.enc


------------------------------
Task 7: Testing
------------------------------
Testing to see if two files "Plaintexts/secret2.txt" and "Plaintexts/secret2.dec" are identical.

Decrypt file: encrypted_secret2.enc 
Cipher: -aes-128-ctr 
Options: -pbkdf2 -iter 64000
Password:$(openssl enc -d -aes-256-cbc -salt -pbkdf2 -iter 64000 -in Passwords/password2_4Bob.enc -pass file:bobpass.txt -md sha256)


The following command is stored in te file: test_share_bob.sh
openssl enc -d -aes-128-ctr -pbkdf2 -iter 64000 -in Ciphertexts/encrypted_secret2.enc \
-pass "pass:$(openssl enc -d -aes-256-cbc -salt -pbkdf2 -iter 64000 -in Passwords/password2_4Bob.enc -pass file:bobpass.txt -md sha256)" \
-out Plaintexts/secret2.dec

# Check to see if the two files differ in content.
diff -q -s Plaintexts/secret2.txt Plaintexts/secret2.dec

