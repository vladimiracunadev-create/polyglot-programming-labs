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
	par := "false"
	if n%2 == 0 {
		par = "true"
	}
	fmt.Printf("entero=%d real=%.1f par=%s\n", n, float64(n), par)
}
