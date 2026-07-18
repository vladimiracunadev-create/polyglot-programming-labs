package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	b, _ := bufio.NewReader(os.Stdin).ReadByte()
	fmt.Printf("char=%c codigo=%d\n", b, b)
}
