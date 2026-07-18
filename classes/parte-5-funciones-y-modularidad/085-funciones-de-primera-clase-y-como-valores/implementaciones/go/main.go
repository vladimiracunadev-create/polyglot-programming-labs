package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func suma(a, b int) int     { return a + b }
func producto(a, b int) int { return a * b }

func aplicar(f func(int, int) int, a, b int) int {
	return f(a, b)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	fields := strings.Fields(line)
	a, _ := strconv.Atoi(fields[0])
	b, _ := strconv.Atoi(fields[1])
	fmt.Printf("suma=%d producto=%d\n", aplicar(suma, a, b), aplicar(producto, a, b))
}
