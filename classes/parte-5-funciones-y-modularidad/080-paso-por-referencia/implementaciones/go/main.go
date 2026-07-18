package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func doblar(p *int) {
	*p *= 2
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	antes := n
	doblar(&n)
	fmt.Printf("antes=%d despues=%d\n", antes, n)
}
