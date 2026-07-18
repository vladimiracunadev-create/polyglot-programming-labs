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
	s := strconv.Itoa(n)
	fmt.Printf("suma=%d texto=%s%s\n", n+n, s, s)
}
