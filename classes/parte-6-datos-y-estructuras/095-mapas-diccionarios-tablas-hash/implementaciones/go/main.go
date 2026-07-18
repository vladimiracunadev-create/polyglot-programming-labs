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
	fields := strings.Fields(line)
	freq := make(map[int]int)
	var nums []int
	for _, s := range fields {
		n, _ := strconv.Atoi(s)
		nums = append(nums, n)
		freq[n]++
	}
	fmt.Printf("cuenta=%d\n", freq[nums[0]])
}
