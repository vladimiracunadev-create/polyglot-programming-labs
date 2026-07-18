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
	var signo string
	switch {
	case n > 0:
		signo = "positivo"
	case n < 0:
		signo = "negativo"
	default:
		signo = "cero"
	}
	fmt.Printf("signo=%s\n", signo)
}
