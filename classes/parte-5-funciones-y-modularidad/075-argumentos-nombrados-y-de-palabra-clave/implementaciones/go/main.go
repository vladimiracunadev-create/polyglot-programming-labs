package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// Go no tiene argumentos nombrados: se usan structs con campos nombrados.
type Punto struct {
	X, Y int
}

func (p Punto) String() string {
	return fmt.Sprintf("punto(x=%d, y=%d)", p.X, p.Y)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	fmt.Println(Punto{X: a, Y: b})
}
