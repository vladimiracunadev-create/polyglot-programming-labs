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
	x, _ := strconv.Atoi(t[0])
	y, _ := strconv.Atoi(t[1])
	var r int
	switch t[2] {
	case "+":
		r = x + y
	case "-":
		r = x - y
	default:
		r = x * y
	}
	fmt.Printf("resultado=%d\n", r)
}
