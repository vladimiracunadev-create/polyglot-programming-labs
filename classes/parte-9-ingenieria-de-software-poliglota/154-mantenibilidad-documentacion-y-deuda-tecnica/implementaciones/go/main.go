package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	mods := strings.Fields(line)
	fmt.Printf("complejidad=%d\n", len(mods))
}
