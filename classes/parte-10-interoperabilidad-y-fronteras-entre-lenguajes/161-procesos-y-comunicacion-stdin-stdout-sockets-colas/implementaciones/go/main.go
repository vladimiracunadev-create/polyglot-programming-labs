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
	recibido := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		recibido += n
	}
	fmt.Printf("recibido=%d\n", recibido)
}
