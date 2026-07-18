package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Forma interface {
	area() int64
}

type Cuadrado struct{ l int64 }
type Rectangulo struct{ a, b int64 }

func (c Cuadrado) area() int64   { return c.l * c.l }
func (r Rectangulo) area() int64 { return r.a * r.b }

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	t := strings.Fields(line)
	var f Forma
	if t[0] == "cuadrado" {
		l, _ := strconv.ParseInt(t[1], 10, 64)
		f = Cuadrado{l}
	} else {
		a, _ := strconv.ParseInt(t[1], 10, 64)
		b, _ := strconv.ParseInt(t[2], 10, 64)
		f = Rectangulo{a, b}
	}
	fmt.Printf("area=%d\n", f.area())
}
