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
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	var parts []string
	suma := 0
	for i := a; i <= b; i++ {
		parts = append(parts, strconv.Itoa(i))
		suma += i
	}
	fmt.Printf("rango=%s suma=%d\n", strings.Join(parts, "-"), suma)
}
