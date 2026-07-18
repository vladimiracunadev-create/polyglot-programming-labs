package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	linea := strings.TrimRight(line, "\r\n")
	palabras := len(strings.Fields(linea))
	fmt.Printf("palabras=%d caracteres=%d\n", palabras, len(linea))
}
