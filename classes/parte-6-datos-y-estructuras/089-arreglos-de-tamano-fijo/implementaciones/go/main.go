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
	var arr [3]int
	for i := 0; i < 3; i++ {
		arr[i], _ = strconv.Atoi(f[i])
	}
	suma, max := 0, arr[0]
	for _, x := range arr {
		suma += x
		if x > max {
			max = x
		}
	}
	fmt.Printf("suma=%d max=%d\n", suma, max)
}
