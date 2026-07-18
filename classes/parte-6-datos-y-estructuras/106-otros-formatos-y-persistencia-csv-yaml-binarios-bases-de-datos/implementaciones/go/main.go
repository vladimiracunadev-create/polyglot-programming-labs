package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	nums := strings.Fields(line)
	fmt.Printf("csv=%s campos=%d\n", strings.Join(nums, ","), len(nums))
}
