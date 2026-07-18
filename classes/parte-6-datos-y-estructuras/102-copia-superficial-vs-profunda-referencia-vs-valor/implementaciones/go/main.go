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
	nums := make([]int, len(f))
	for i, s := range f {
		nums[i], _ = strconv.Atoi(s)
	}
	copia := make([]int, len(nums))
	copy(copia, nums)
	copia[len(copia)-1] = 99
	fmt.Printf("original=%s copia=%s\n", join(nums), join(copia))
}

func join(a []int) string {
	parts := make([]string, len(a))
	for i, n := range a {
		parts[i] = strconv.Itoa(n)
	}
	return strings.Join(parts, "-")
}
