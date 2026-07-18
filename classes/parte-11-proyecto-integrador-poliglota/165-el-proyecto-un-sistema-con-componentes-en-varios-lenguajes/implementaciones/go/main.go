package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	c := strings.Fields(line)
	fmt.Printf("componentes=%d nombres=%s\n", len(c), strings.Join(c, "-"))
}
