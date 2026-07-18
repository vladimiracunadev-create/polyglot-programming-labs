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
	t := strings.Fields(line)
	a, _ := strconv.Atoi(t[0])
	b, _ := strconv.Atoi(t[2])
	var r int
	switch t[1] {
	case "+":
		r = a + b
	case "-":
		r = a - b
	default:
		r = a * b
	}
	fmt.Printf("resultado=%d\n", r)
}
