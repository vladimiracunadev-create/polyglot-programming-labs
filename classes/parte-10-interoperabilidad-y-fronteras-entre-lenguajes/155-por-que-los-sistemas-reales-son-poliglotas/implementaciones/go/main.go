package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	comps := strings.Fields(line)
	fmt.Printf("componentes=%d\n", len(comps))
}
