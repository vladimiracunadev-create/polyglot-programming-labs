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
	verde := true
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		if n != 1 {
			verde = false
		}
	}
	res := "rojo"
	if verde {
		res = "verde"
	}
	fmt.Printf("ci=%s\n", res)
}
