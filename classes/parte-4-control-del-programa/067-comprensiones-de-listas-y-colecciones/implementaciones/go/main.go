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
	var pares []string
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		if n%2 == 0 {
			pares = append(pares, strconv.Itoa(n))
		}
	}
	fmt.Printf("pares=%s\n", strings.Join(pares, "-"))
}
