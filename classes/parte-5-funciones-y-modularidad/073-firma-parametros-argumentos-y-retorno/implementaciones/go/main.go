package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func suma(a, b int) int {
	return a + b
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	fmt.Printf("suma=%d\n", suma(a, b))
}
