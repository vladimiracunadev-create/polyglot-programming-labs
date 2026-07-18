package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	rev := make([]string, len(f))
	for i, x := range f {
		rev[len(f)-1-i] = x
	}
	fmt.Printf("pila=%s cola=%s\n", strings.Join(rev, "-"), strings.Join(f, "-"))
}
