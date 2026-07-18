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
	var r int64 = 1
	for i := 0; i < n; i++ {
		r *= 2
	}
	fmt.Printf("resultado=%d\n", r)
}
