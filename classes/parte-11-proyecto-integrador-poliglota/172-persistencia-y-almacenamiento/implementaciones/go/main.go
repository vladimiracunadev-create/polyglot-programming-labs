package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	p := strings.Fields(line)
	almacen := map[string]string{}
	almacen[p[0]] = p[1]
	fmt.Printf("guardado=%s=%s\n", p[0], almacen[p[0]])
}
