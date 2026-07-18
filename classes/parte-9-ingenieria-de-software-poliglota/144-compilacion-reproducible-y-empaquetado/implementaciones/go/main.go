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
	c := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		c += n
	}
	fmt.Printf("checksum=%d\n", c)
}
