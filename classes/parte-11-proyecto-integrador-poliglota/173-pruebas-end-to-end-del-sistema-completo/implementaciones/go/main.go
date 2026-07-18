package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	e, _ := strconv.Atoi(f[2])
	res := "falla"
	if a+b == e {
		res = "pasa"
	}
	fmt.Printf("e2e=%s\n", res)
}
