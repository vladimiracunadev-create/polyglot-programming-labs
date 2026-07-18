package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func hacerSumador(base int) func(int) int {
	return func(x int) int {
		return base + x
	}
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	base, _ := strconv.Atoi(strings.TrimSpace(line))
	sumar := hacerSumador(base)
	fmt.Printf("r1=%d r2=%d\n", sumar(1), sumar(2))
}
