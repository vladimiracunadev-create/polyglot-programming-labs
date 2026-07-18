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
	if n > 0 {
		fmt.Printf("resultado=%d\n", n*2)
	} else {
		fmt.Println("resultado=nada")
	}
}
