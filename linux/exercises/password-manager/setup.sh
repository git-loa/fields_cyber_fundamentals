# Ensure script is run as rooot
if [[$EUID -ne 0]]; 
then
   echo "This script must be run as root"
   exit 1
fi


# Create password manager group
echo "Creating password manager group..."
sudo groupadd password-manager

# Add current user to password manager group
echo "Adding user to password manager group..."
sudo usermod -a -G password-manager $USER

# Change ownership of the data directory...
echo "Changing ownership of the data directory..." 
sudo chown -R $USER:password-manager data/

# Set permissions for the data directory 
echo "Setting permissions for the data directory..." 
chmod 770 data/ 
chmod 770 data/passwords/ 
echo "Setup complete. Please log out and log back in for group changes to take effect." 