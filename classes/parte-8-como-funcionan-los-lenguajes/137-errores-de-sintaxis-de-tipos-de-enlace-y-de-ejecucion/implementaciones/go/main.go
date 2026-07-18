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
	codigo, _ := strconv.Atoi(strings.TrimSpace(line))
	var e string
	switch codigo {
	case 1:
		e = "sintaxis"
	case 2:
		e = "tipos"
	case 3:
		e = "enlace"
	case 4:
		e = "ejecucion"
	default:
		e = "desconocido"
	}
	fmt.Printf("error=%s\n", e)
}
