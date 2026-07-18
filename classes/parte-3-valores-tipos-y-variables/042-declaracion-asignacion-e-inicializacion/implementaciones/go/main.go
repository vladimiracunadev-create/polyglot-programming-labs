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
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])

	// Go permite intercambio con asignación múltiple.
	a, b = b, a

	fmt.Printf("a=%d b=%d\n", a, b)
}
