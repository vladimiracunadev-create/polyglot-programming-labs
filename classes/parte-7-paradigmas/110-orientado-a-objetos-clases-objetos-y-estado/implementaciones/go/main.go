package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Contador struct {
	cuenta int
}

func (c *Contador) incrementar() {
	c.cuenta++
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	c := &Contador{}
	for i := 0; i < n; i++ {
		c.incrementar()
	}
	fmt.Printf("cuenta=%d\n", c.cuenta)
}
