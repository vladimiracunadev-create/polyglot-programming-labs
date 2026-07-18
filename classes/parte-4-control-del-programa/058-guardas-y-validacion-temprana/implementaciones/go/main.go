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
	edad, _ := strconv.Atoi(strings.TrimSpace(line))
	if edad < 0 {
		fmt.Println("invalido")
		return
	}
	if edad < 18 {
		fmt.Println("menor")
		return
	}
	fmt.Println("adulto")
}
