package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func doblar(x int) int {
	x = x * 2
	return x
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	local := doblar(n)
	fmt.Printf("original=%d local=%d\n", n, local)
}
