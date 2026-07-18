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
	var stream []string
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		if n%2 == 0 {
			stream = append(stream, strconv.Itoa(n*2))
		}
	}
	fmt.Printf("stream=%s\n", strings.Join(stream, "-"))
}
