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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	// Go usa goroutines y canales en lugar de async/await.
	ch := make(chan int, 1)
	go func() { ch <- n * 2 }()
	fmt.Printf("resultado=%d\n", <-ch)
}
