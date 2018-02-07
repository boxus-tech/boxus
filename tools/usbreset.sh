# It works, but quite weird. May totally freeze a device
sudo sh -c "echo 0 > /sys/bus/usb/devices/1-1.5:1.0/authorized"
sudo sh -c "echo 1 > /sys/bus/usb/devices/1-1.5:1.0/authorized"
