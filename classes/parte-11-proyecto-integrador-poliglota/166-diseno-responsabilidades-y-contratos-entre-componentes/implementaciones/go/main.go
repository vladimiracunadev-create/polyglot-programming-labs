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
	res := "incompatible"
	if f[0] == f[1] {
		res = "compatible"
	}
	fmt.Printf("contrato=%s\n", res)
}
