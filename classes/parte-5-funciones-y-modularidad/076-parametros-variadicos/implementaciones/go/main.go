package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func suma(nums ...int) int {
	total := 0
	for _, n := range nums {
		total += n
	}
	return total
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	var nums []int
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		nums = append(nums, n)
	}
	fmt.Printf("suma=%d\n", suma(nums...))
}
