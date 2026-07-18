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
	t := strings.Fields(line)
	indice, _ := strconv.Atoi(t[0])
	lista := t[1:]
	fmt.Printf("valor=%s\n", lista[indice])
}
