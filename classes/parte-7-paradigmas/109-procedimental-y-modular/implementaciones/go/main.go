package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func promedio(a []int) int {
	suma := 0
	for _, x := range a {
		suma += x
	}
	return suma / len(a)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	var nums []int
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		nums = append(nums, n)
	}
	fmt.Printf("promedio=%d\n", promedio(nums))
}
