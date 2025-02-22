#!/bin/bash

###########################################################################
#############     Functionality to Create and Store Passwords   ###########
###########################################################################

# Password Generation Function
generate_password() {
   local random_password=$(openssl rand -base64 24)
   echo -n "$random_password"
}

# Password encryption
encrypt_password() {
    local master_password="$1"
    local random_password="$2"

    encrypted_password=$(echo -n "$random_password" | openssl enc \
    -aes-256-cbc -a -pbkdf2 -iter 64000 -pass pass:"$master_password")

    echo -n "$encrypted_password"
}

# New Password Creation
new_password() {
    master_password="$1"
    mkdir -p data/passwords

    # Prompts user for account name
    while true;
    do
        read -p "Enter account name to proceed (or 'q' to quit): " account_name && echo
        if [ "${account_name}" == "q" ];
        then
            echo "Returning to main menu..."
            return
        fi

        if [ -f "data/passwords/${account_name}" ];
        then
            read -p "A password already exists for ${account_name}. Overwrite? (y/n): " \
            overwrite
            if [ "${overwrite}" != "y" ];
            then
                echo "Choose a different account name (or enter 'q' to quit.)"
                continue
            fi
        fi
        read -p "Confirm account name '${account_name}' (y/n): " confirm
        if [ "${confirm}" != "y" ];
        then
            echo "Let's try again."
            continue
        fi

        # Generating a random password with  the function generate_password
        local generated_password=$(generate_password)
        #echo "Generated Password: ####### $generated_password"
        encrypted_password=$(encrypt_password "$MASTER_PASSWORD" "$generated_password")
        # echo $encrypted_password
        # Save encrypted password to data/passwords
        echo "Saving encrypted password..."
        sleep 1s
        echo "Saved successfully."
        echo -n "${encrypted_password}" > data/passwords/"${account_name}"

        break
    done
}


#######################################################################
############            Password Retrieval Section        #############
#######################################################################

# Password Decryption
decrypt_password() {
    master_password="$1"
    ciphertext="$2"
    decrypted_password=$(echo -n "$ciphertext" | openssl enc -d \
    -aes-256-cbc -a -pbkdf2 -iter 64000 -pass pass:"$master_password")
    
    echo -n "$decrypted_password"
}

# Password Display
display_password() {
    echo "Password: $1"
    read -p "Press Enter of return key when done viewing password..."
    clear
}

# Password Retrieval
retrieve_password() {
    local master_password="$1"

    # Check if data/passwords is empty; return 1 if empty
    if [ -z "$(ls -A 'data/passwords')" ];
    then
        echo "No passwords saved. Returning to main menu..."
        sleep 1s
        clear
        return 1
    fi


    # Prompts user for account name
    while true;
    do
        read -p "Enter your account name: " account_name && echo
        if [ ! -f "data/passwords/${account_name}" ];
        then
            echo "The account '${account_name}' does not exits"
            read -p "Do you want to quit (y/n)?: " quit && echo
            if [ "$quit" == "y" ];
            then
                return 0
            else
                continue
            fi
        fi

        local encrypted_password=$(< "data/passwords/$account_name")
        
        local decrypted_password=$(decrypt_password "$master_password" "$encrypted_password")
        
        display_password "$decrypted_password"

        break 
    done
}



## End of Exercise





#######################################################################
############   Exploring some of the ideas suggested      #############
#######################################################################


authenticate_with_master_password(){
    local master_password="$1"
    local password_hash=$(cat data/.MASTER)
    local password_salt=$(echo $password_hash | cut -d '$' -f3)
    
    local user_hash=$(openssl passwd -6 -salt "$password_salt" "$master_password")

    if [ "$password_hash" == "$user_hash" ];
    then
        return 0
    else
        return 1
    fi    
}


delete_password(){
    local master_password
    local attempts=0 max_attempts=3

    ###################    START AUTHENTICATION    ######################
    
    # Prompt user for master password with limited number of attempts
    

    while [ "$attempts" -lt "$max_attempts" ]
    do
        read -sp "Enter the master password for authentication: " master_password && echo
        if authenticate_with_master_password "$master_password";
        then
            break
        fi

        echo "Incorrect master password. Please Try again."
        attempts=$((attempts+1))
    done

    # Exit if maximum attempts are reached.
    if [ "$attempts" -ge "$max_attempts" ];
    then
        echo "Maximum attepmts reaching. Retuning to main menu..."
        sleep 2s
        return 1
    fi
    ####################    END AUTHENTICATION    ######################




    ####################    START DELETION     ######################

    # Check if data/passwords is empty
    if [ -z "$(ls -A data/passwords)" ];
    then
        echo "No passwords saved. Returning to main menu..."
        sleep 1s
        clear
        return 1
    fi

    # Detele an account
    while true
    do
        read -p "Enter the account name to delete (or 'q' to quit): " account_name && echo
        # Enter 'q' to quit
        if [ "$account_name" == "q" ]; then
            return 0
        fi

        # Check if account name exists.
        if [ ! -f "data/passwords/${account_name}" ];
        then
            echo "The account '${account_name}' does nor exist."
            continue
        fi

        read -p "Are you sure you want to delete the password for '${account_name}' (y/n): " confirm_delete && echo

        case "$confirm_delete" in 
            y|Y)
                echo "Deleting password for for '${account_name}'..."
                rm -f "data/passwords/${account_name}"
                echo "Password for '${account_name}' has been deleted."
                sleep 2s
                return 0
                ;;
            n|N) 
                echo "Deletion aborted." 
                sleep 2s
                return 0 
                ;;
            *)
                echo "Invalid option. Please try again"
                ;;
        esac
    done
}
    ################          END DELETION           ####################


change_master_password() {
    #################        CHANGE MASTER PASSWORD     ################# 
    local old_master_password
    local new_master_password1 new_master_password2
    local account_name
    local encrypt_password decrypt_password

    # Authenticate the old master password 
    read -sp "Enter current master password: " old_master_password && echo 
    if ! authenticate_with_master_password "$old_master_password"; then 
        echo "Incorrect master password." 
        return 1 
    fi
    
    # Set a new master password
    echo "Set  a new master password."
    while true 
    do
        read -sp "Enter new master password: " new_master_password1 && echo
        read -sp "Re-enter new master password: " new_master_password2 && echo
        if [ "$new_master_password1" == "$new_master_password2" ]; then
            new_master_password="$new_master_password1"
            break
        fi

        echo "Passwords do not match. Please try again."
    done

    # Re-encrypt all the stored passwords with the new master password
    for account_name in "data/passwords"/*; do
        cat "$account_name"
        encrypted_password=$(<"${account_name}")
        decrypted_password=$(decrypt_password "$old_master_password" "$encrypted_password")
        new_encrypted_password=$(encrypt_password "$new_master_password" "$decrypted_password")
    done

    # Save new master password 
    echo -n $(openssl passwd -6 -salt "$(openssl rand -base64 16)" "$new_master_password") > data/.MASTER
    echo "Changing current master password..." 
    sleep 3s
    echo "Master password has been successfully changed."
    sleep 3s
}