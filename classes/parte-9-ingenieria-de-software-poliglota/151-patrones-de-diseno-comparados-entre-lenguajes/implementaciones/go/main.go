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
	t := strings.Fields(line)
	a, _ := strconv.Atoi(t[1])
	b, _ := strconv.Atoi(t[2])
	ops := map[string]int{"suma": a + b, "resta": a - b, "producto": a * b}
	fmt.Printf("resultado=%d\n", ops[t[0]])
}
