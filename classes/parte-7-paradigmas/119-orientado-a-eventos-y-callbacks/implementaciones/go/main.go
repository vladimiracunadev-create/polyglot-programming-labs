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
	var recolectados []string
	alEvento := func(i int) {
		recolectados = append(recolectados, strconv.Itoa(i))
	}
	for i := 1; i <= n; i++ {
		alEvento(i)
	}
	fmt.Printf("eventos=%s\n", strings.Join(recolectados, "-"))
}
