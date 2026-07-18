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
	suma := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		suma += n
	}
	fmt.Printf("suma=%d\n", suma)
}
