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
	d, _ := strconv.Atoi(strings.TrimSpace(line))
	var dia string
	switch d {
	case 1:
		dia = "lunes"
	case 2:
		dia = "martes"
	case 3:
		dia = "miercoles"
	case 4:
		dia = "jueves"
	case 5:
		dia = "viernes"
	case 6:
		dia = "sabado"
	case 7:
		dia = "domingo"
	default:
		dia = "invalido"
	}
	fmt.Printf("dia=%s\n", dia)
}
