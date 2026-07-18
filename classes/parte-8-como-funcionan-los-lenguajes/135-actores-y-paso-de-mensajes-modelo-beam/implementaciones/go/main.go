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
	buzon := make(chan int, 64)
	done := make(chan int64)
	go func() { // actor: acumula los mensajes de su buzón
		var total int64
		for m := range buzon {
			total += int64(m)
		}
		done <- total
	}()
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		buzon <- n
	}
	close(buzon)
	fmt.Printf("total=%d\n", <-done)
}
