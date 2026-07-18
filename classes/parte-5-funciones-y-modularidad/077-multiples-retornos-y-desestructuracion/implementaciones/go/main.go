package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func divmod(a, b int) (int, int) {
	return a / b, a % b
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	q, r := divmod(a, b)
	fmt.Printf("cociente=%d resto=%d\n", q, r)
}
