package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	msgs := strings.Fields(line)
	fmt.Printf("commits=%d\n", len(msgs))
}
