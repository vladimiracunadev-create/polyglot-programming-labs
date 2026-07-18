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
	total := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		total += n
	}
	fmt.Printf("total=%d\n", total)
}
