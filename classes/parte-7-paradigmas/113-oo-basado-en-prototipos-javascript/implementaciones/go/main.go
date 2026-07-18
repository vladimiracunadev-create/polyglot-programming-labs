package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Obj struct{ valor int }

func (o Obj) doble() int { return o.valor * 2 }

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	o := Obj{valor: n}
	fmt.Printf("resultado=%d\n", o.doble())
}
