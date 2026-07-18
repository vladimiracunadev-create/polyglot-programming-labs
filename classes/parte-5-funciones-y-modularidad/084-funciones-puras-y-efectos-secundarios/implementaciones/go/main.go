package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func cuadrado(n int64) int64 {
	return n * n
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	fmt.Printf("puro=%d\n", cuadrado(n))
}
