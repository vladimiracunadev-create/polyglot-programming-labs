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
	suma := 0
	i := 1
	for i <= n {
		suma += i
		i++
	}
	fmt.Printf("suma=%d\n", suma)
}
