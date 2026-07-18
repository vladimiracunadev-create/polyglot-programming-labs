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
	var doblados []string
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		doblados = append(doblados, strconv.Itoa(n*2))
	}
	fmt.Printf("doblados=%s\n", strings.Join(doblados, "-"))
}
