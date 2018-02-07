/*
 *
 * Program to reset USB device equivalently to plug out/plug in
 * 
 * It throws following errors:
 * pi@RaspberryPi:~ $ sudo ./usbreset /dev/video0
 * > Error while opening device file: Device or resource busy
 * > Error in ioctl: Bad file descriptor
 * but still causes effective device reset (TODO Why???)
 * 
*/

#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/ioctl.h>

#include <linux/usbdevice_fs.h>

int main(int argc, char **argv)
{
    const char *devpath;
    int fd;
    int rc;

    if (argc != 2) {
        fprintf(stderr, "Usage: ./usbreset /dev/device-filename\n");
        return 1;
    }
    devpath = argv[1];

    /* 
     * In order to use this call, one needs an open file descriptor.  Often
     * the open(2) call has unwanted side effects, that can be avoided under
     * Linux by giving it the O_NONBLOCK flag.
     * 
     * From here http://man7.org/linux/man-pages/man2/ioctl.2.html
     */
    fd = open(devpath, O_NONBLOCK);
    if (fd < 0) {
        perror("Error while opening device file");
    }

    rc = ioctl(fd, USBDEVFS_RESET, 0);
    if (rc < 0) {
        perror("Error in ioctl");
    }

    printf("Device %s reset successful\n", devpath);

    close(fd);
    return 0;
}
