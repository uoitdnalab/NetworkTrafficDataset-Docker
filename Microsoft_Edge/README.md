# Microsoft Edge

Builds a Docker container for interacting with a QEMU-KVM virtual
machine running the Microsoft Edge browser in Windows 10.

Before Running
--------------

- Create in the `HelperContainer` directory the FIFO Pipe `capture_ctrl`
- Open the file `docker-compose.yml` and edit the line
`/dev/null:/qemu_host_pty` replacing `/dev/null` with QEMU Monitor's
PTY.
