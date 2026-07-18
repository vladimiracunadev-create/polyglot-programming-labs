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
	esperado, _ := strconv.Atoi(f[2])
	res := "falla"
	if a+b == esperado {
		res = "pasa"
	}
	fmt.Printf("test=%s\n", res)
}
