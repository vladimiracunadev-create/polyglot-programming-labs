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
	v := strings.Split(strings.TrimSpace(line), ".")
	ma, _ := strconv.Atoi(v[0])
	me, _ := strconv.Atoi(v[1])
	pa, _ := strconv.Atoi(v[2])
	fmt.Printf("mayor=%d menor=%d parche=%d\n", ma, me, pa)
}
