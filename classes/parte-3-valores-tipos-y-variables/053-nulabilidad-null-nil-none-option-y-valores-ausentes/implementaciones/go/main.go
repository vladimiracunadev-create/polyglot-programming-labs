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
	if n == 0 {
		fmt.Println("valor=ausente")
	} else {
		fmt.Printf("valor=%d\n", n)
	}
}
