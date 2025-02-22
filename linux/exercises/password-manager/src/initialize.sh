#!/bin/bash

# Global variables
MASTER_PASSWORD=""


initialize() {
    echo ""
    echo "Welcome to the password manager." && echo
    
    if [ -f "data/.MASTER" ];
    then
        check_master_password
    else
        create_master_pasword
    fi
}

create_master_pasword(){
    echo "Creating master password..."
    echo ""
    while true;
    do
        read -sp "Enter  master password: " master_password1 && echo
        read -sp "Re-enter master password: " master_password2 && echo
        echo ""
        # Password verification
        if [ "${master_password1}" == "${master_password2}" ];
        then
            echo "Passwords match and program is starting..."
            sleep 1s
            echo ""
            MASTER_PASSWORD="${master_password1}"
            
            # Generate a hashed password using openssl passwd
            echo -n $(openssl passwd -6 -salt "$(openssl rand -base64 16)" \
            "${MASTER_PASSWORD}") > data/.MASTER
            break
        else
            echo "Passwords do not match. Please try again."
            echo ""
        fi
    done
    
}

# Function to extract salt from a hashed password.
get_salt(){
    salt=$(echo $1 | cut -d '$' -f3)
    echo -n ${salt}
}

check_master_password(){
    password_hash=$(cat data/.MASTER)
    password_salt=$(get_salt "${password_hash}")

    while true;
    do
        read -sp "Enter master password: " password && echo
        MASTER_PASSWORD="${password}"
        local user_hash=$(openssl passwd -6 -salt "${password_salt}" "${MASTER_PASSWORD}")

        if [ "${password_hash}" == "${user_hash}" ];
        then
            break
        else
            echo "Incorrect password. Please try again."
            echo ""
        fi
    done
    return 0
}
