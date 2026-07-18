package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func tf(x bool) string {
	if x {
		return "true"
	}
	return "false"
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	pos := n > 0
	par := n%2 == 0
	fmt.Printf("positivo=%s par=%s ambos=%s\n", tf(pos), tf(par), tf(pos && par))
}
