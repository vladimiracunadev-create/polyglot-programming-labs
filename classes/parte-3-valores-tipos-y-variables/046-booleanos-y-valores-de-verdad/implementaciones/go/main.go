package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func tf(x bool) string {
	if x {
		return "true"
	}
	return "false"
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	ai, _ := strconv.Atoi(f[0])
	bi, _ := strconv.Atoi(f[1])
	a, b := ai != 0, bi != 0
	fmt.Printf("and=%s or=%s not_a=%s\n", tf(a && b), tf(a || b), tf(!a))
}
