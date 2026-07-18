package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	var mu sync.Mutex
	cuenta := 0
	for i := 0; i < n; i++ {
		mu.Lock()
		cuenta++
		mu.Unlock()
	}
	fmt.Printf("cuenta=%d\n", cuenta)
}
