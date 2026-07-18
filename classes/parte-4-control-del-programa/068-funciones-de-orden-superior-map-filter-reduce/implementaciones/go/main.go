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
	total := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		d := n * 2
		doblados = append(doblados, strconv.Itoa(d))
		total += d
	}
	fmt.Printf("doblados=%s total=%d\n", strings.Join(doblados, "-"), total)
}
