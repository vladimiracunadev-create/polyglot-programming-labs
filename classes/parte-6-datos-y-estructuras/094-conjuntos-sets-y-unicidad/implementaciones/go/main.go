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
	set := make(map[int]struct{})
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		set[n] = struct{}{}
	}
	fmt.Printf("unicos=%d\n", len(set))
}
