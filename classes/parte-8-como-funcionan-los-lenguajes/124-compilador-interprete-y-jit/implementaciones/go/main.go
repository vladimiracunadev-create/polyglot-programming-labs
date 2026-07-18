package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n := strings.TrimSpace(line)
	fmt.Printf("digitos=%d\n", len(n))
}
