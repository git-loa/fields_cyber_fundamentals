#!/bin/bash

# include
source src/initialize.sh
source src/passwords.sh
source src/utils.sh

show_menu() {
    echo "Password Manager Menu"
    echo "---------------------"
    echo "1. Add new password"
    echo "2. Get password"
    echo "3. List accounts"
    echo "4. Delete password"
    echo "5. Change master password"
    echo "6. Exit"
    echo ""

    read -p "Choose an option from the above menu (1 \| 2, \| 3 \| 4 \| 5 \| 6): " menu_option
    
    case $menu_option in
        1)
            echo "Add new password"
            new_password "${MASTER_PASSWORD}"
            echo ""
            sleep 2s
            ;;
        2)
            echo "Get password"
            retrieve_password "$MASTER_PASSWORD"
            echo ""
            
            ;;
        3)
            echo "List accounts"
            echo ""
            list_accounts
            echo ""
            
            ;;
        4)
            echo "Delete Password"
            echo ""
            delete_password
            echo ""
            
            ;;
        5)
            echo "Change Master Password"
            echo ""
            change_master_password
            echo ""
            
            ;;
        6)
            echo "You chose option 4: Exit"
            read -p "Are you sure you want to exit? (y/n): " confirm_exit
            case $confirm_exit in
                y|Y)
                    echo "You are exiting the program.."
                    sleep 0.5s
                    echo "Goodbye!"
                    sleep 2.5s
                    clear
                    exit 0
                    ;;
                n|N)
                    echo "Returning to menu."
                    echo ""
                    
                    ;;
                *)
                    echo "Invalid option. Returning to menu."
                    echo ""
                    ;;
            esac
            ;;
        *)
            echo "Invalid option. Please choose a valid option."
            echo ""
            ;;
    esac
    
}

main() {
    # Main function will be implemented in later exercises

    initialize
    # echo $MASTER_PASSWORD
    while true;
    do
        clear
        echo
        echo "             #####################################################################"
        echo "             ###################  Password Manager by Leonard.  ##################"
        echo "             #####################################################################"
        echo ""
        show_menu
    done
}

# You many choose to  parse arguments lo the main function
main "$@"
    
