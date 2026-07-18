package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// Go no tiene defectos: se simula con la lógica de llamada.
func potencia(base int64, exp int) int64 {
	var r int64 = 1
	for i := 0; i < exp; i++ {
		r *= base
	}
	return r
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	t := strings.Fields(line)
	base, _ := strconv.ParseInt(t[0], 10, 64)
	exp := 2
	if len(t) > 1 {
		exp, _ = strconv.Atoi(t[1])
	}
	fmt.Printf("resultado=%d\n", potencia(base, exp))
}
