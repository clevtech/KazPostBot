sudo apt-get install -y freenect
sudo modprobe -r gspca_kinect 
sudo modprobe -r gspca_main
echo "blacklist gspca_kinect" |sudo tee -a /etc/modprobe.d/blacklist.conf
sudo adduser $USER plugdev
sudo apt install -y python3 python3-dev python3-pip python-pip python-dev bluez libglib2.0-dev build-essential git cmake python-freenect libusb-1.0-0-dev
sudo pip3 install bluepy telepot flask 
sudo add-apt-repository ppa:webupd8team/atom
sudo apt update
sudo apt install -y atom
echo "Done"

