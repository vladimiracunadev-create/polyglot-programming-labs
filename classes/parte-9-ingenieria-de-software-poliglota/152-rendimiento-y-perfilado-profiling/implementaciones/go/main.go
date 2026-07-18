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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	ops, suma := 0, 0
	for i := 1; i <= n; i++ {
		suma += i
		ops++
	}
	fmt.Printf("operaciones=%d resultado=%d\n", ops, suma)
}
