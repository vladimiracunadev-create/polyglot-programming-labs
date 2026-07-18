package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// En un proyecto real 'doble' viviría en otro paquete; aquí simula el módulo.
func doble(n int) int {
	return 2 * n
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("resultado=%d\n", doble(n))
}
