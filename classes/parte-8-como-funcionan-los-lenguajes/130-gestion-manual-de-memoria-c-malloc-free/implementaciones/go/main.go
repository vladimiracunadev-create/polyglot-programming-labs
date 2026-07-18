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
	arr := make([]int, n)
	suma := 0
	for i := 0; i < n; i++ {
		arr[i] = i + 1
		suma += arr[i]
	}
	fmt.Printf("reservado=%d suma=%d\n", n, suma)
}
