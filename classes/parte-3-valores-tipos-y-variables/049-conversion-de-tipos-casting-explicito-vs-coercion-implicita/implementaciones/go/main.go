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
	f, _ := strconv.ParseFloat(strings.TrimSpace(line), 64)
	fmt.Printf("entero=%d real=%.2f\n", int64(f), f)
}
