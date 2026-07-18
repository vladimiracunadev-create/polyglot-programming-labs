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
	var f int64 = 1
	for i := 1; i <= n; i++ {
		f *= int64(i)
	}
	fmt.Printf("factorial=%d\n", f)
}
