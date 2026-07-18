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
	valor := 0
	func() {
		defer func() { /* se libera al salir */ }()
		valor = n
	}()
	fmt.Printf("valor=%d estado=liberado\n", valor)
}
