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
	acc := 0
	var pasos []string
	for i := 1; i <= n; i++ {
		acc += i
		pasos = append(pasos, strconv.Itoa(acc))
	}
	fmt.Printf("traza=%s\n", strings.Join(pasos, "-"))
}
