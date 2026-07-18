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
	var nums []int
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		nums = append(nums, n)
	}
	medio := len(nums) / 2
	ch := make(chan int, 2)
	sumar := func(parte []int) {
		s := 0
		for _, x := range parte {
			s += x
		}
		ch <- s
	}
	go sumar(nums[:medio])
	go sumar(nums[medio:])
	s1 := <-ch
	s2 := <-ch
	fmt.Printf("suma=%d\n", s1+s2)
}
