package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func sumar(n int) int64 {
	if n == 0 {
		return 0
	}
	return int64(n) + sumar(n-1)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("suma=%d profundidad=%d\n", sumar(n), n)
}
