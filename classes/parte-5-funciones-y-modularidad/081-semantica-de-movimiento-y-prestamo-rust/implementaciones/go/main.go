package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	s := strings.TrimSpace(line)
	longitud := len(s) // GC: sin propiedad explícita.
	fmt.Printf("movido=%s longitud=%d\n", s, longitud)
}
