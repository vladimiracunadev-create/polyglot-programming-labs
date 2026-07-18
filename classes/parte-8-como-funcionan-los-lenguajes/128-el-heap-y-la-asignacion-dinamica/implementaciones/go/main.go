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
	var lista []string
	for i := n; i >= 1; i-- {
		lista = append(lista, strconv.Itoa(i))
	}
	fmt.Printf("lista=%s\n", strings.Join(lista, "-"))
}
