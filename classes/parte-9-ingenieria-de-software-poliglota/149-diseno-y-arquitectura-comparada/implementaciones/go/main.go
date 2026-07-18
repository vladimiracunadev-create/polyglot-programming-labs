package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	capas := strings.Fields(line)
	fmt.Printf("capas=%d\n", len(capas))
}
