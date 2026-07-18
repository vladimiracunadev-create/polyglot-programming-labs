package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func fib(n int) int64 {
	if n < 2 {
		return int64(n)
	}
	return fib(n-1) + fib(n-2)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("fib=%d\n", fib(n))
}
