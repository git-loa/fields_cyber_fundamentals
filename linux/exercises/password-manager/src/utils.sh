#!/bin/bash

list_accounts(){
    if [ -z "$(ls -A data/passwords)" ];
    then
    echo ""
        echo "There are no saved passwords. Please add a password."
        return 1
    fi
    echo "  Accounts: "
    echo "--------------"
    ls -1 data/passwords
    echo ""
    read -p "Press Enter of the return key to return to the main menu."
}
