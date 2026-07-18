package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	res := "false"
	if f[0] == f[1] {
		res = "true"
	}
	fmt.Printf("equivalente=%s\n", res)
}
