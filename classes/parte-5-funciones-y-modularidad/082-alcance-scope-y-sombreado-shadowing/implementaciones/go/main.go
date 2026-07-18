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
	x := n
	{
		x := n + 10 // sombrea a la externa en este bloque
		fmt.Printf("interno=%d externo=%d\n", x, n)
	}
}
