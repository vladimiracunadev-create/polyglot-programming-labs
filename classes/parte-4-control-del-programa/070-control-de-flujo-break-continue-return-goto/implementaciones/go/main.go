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
	d := 2
	for ; d <= n; d++ {
		if n%d == 0 {
			break
		}
	}
	fmt.Printf("primer_divisor=%d\n", d)
}
