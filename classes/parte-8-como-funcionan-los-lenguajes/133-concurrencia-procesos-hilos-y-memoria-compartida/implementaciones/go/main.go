package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	cuenta := 0
	for range strings.Fields(line) {
		cuenta++
	}
	fmt.Printf("cuenta=%d\n", cuenta)
}
