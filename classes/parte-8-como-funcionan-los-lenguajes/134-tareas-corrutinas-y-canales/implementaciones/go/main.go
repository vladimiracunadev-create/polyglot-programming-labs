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
	f := strings.Fields(line)
	ch := make(chan int, len(f))
	go func() { // productor
		for _, s := range f {
			n, _ := strconv.Atoi(s)
			ch <- n
		}
		close(ch)
	}()
	primero := true
	maximo := 0
	for x := range ch { // consumidor
		if primero || x > maximo {
			maximo = x
			primero = false
		}
	}
	fmt.Printf("max=%d\n", maximo)
}
