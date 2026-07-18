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
	x := n // externo
	interno := 0
	{
		x := x + 10 // sombrea a la externa en este bloque
		interno = x
	}
	fmt.Printf("interno=%d externo=%d\n", interno, x)
}
