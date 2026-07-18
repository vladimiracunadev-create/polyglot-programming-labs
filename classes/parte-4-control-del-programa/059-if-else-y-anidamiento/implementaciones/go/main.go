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
	score, _ := strconv.Atoi(strings.TrimSpace(line))
	var nota string
	if score >= 90 {
		nota = "A"
	} else if score >= 80 {
		nota = "B"
	} else if score >= 70 {
		nota = "C"
	} else {
		nota = "F"
	}
	fmt.Printf("nota=%s\n", nota)
}
