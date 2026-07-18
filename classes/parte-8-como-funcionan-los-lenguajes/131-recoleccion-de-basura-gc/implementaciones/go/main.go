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
	for i := 0; i < n; i++ {
		tmp := new(int) // sin referencia persistente, el GC lo recolecta
		_ = tmp
	}
	fmt.Printf("creados=%d estado=recolectado\n", n)
}
